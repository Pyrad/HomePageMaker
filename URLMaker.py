import re
import os
import shutil


class URLMaker:
    def __init__(self, url_list_file, default_img="github120x120.png", ncolumn=4):
        """
        Constructor of class URLMaker
        :param url_list_file: A file which contains a list of URLs
        :param ncolumn: How many icon/URL for a row to have on the page (body), default is 4
        """
        self.url_file = url_list_file
        self.ncol = ncolumn
        self.dbg_row_limit = -1
        self.body_file = None
        self.index_file_head = "index_part_head.html"
        self.index_file_tail = "index_part_tail.html"
        self.default_img = default_img # For those without any image description
        self.url_number = 0
        # keep all the icons used, to copy to a customized directory
        self.icon_list = []
        self.final_index_html = None
        # To get URL information from file "classified_urls.html"
        self.section_dict = None

    def reset(self):
        self.dbg_row_limit = -1
        self.body_file = None
        self.url_number = 0
        self.icon_list = []
        self.final_index_html = None

    @staticmethod
    def row_start_label():
        return r'<div class="row">'

    @staticmethod
    def row_end_label():
        return r'</div>'

    @staticmethod
    def check_file_exists(fname):
        """
        Checks if a file exists
        :param fname: The file to check
        :return: True if it exists, otherwise False
        """
        return True if os.path.isfile(fname) else False

    @staticmethod
    def check_dir_exist(fdir):
        """
        Checks if a directory exists
        :param fdir: A directory name
        :return: True if it exists, otherwise False
        """
        return True if os.path.isdir(fdir) else False

    def generate_body_rows(self, outfname="url.cols.html"):
        """
        Generate the main page body which contains the URLs
        :param outfname the file name to write out
        :return: If the outfname is successfully written out
        """

        # First all of first, reset some internal variables
        self.reset()

        # First check if the URL list file exists
        fname = self.url_file
        if not URLMaker.check_file_exists(fname):
            print("Error, file not found:", fname)
            return

        #outfname = "url.cols.html"
        outf = open(outfname, "w", encoding='utf-8')

        dbg_cnt = 0

        #url_pattern = re.compile(r'.*data-url="(\S+)".*title="(\S+)"')
        url_pattern = re.compile(r'data-url="(.*)"')
        title_pattern = re.compile(r'title="(.*)"')
        img_pattern = re.compile(r'image="(.*)"')

        line_cnt, real_line_cnt, colcnt = 0, 0, 0

        with open(fname, 'r', encoding='utf-8') as f:
            for line in f.readlines():
                line_cnt += 1
                l = line.strip()
                if len(l) == 0 or l.startswith("<!--"):
                    continue
                if not l.startswith("data-url"):
                    continue

                kwlist = l.split(",")

                assert len(kwlist) == 2 or len(kwlist) == 3

                url_m = url_pattern.match(kwlist[0].strip())
                title_m = title_pattern.match(kwlist[1].strip())
                img_m = img_pattern.match(kwlist[2].strip()) if len(kwlist) == 3 else None

                if url_m is None or title_m is None:
                    continue
                str_url = url_m.group(1)
                str_webname = title_m.group(1)
                str_imgf = "undef128x128.png" if img_m is None else img_m.group(1)
                str_imgf = "undef128x128.png" if len(str_imgf) == 0 else str_imgf
                str_descri = str_webname

                # Keep icon names
                if str_imgf != "undef128x128.png" and not str_imgf in self.icon_list:
                    self.icon_list.append(str_imgf)

                dbg_cnt += 1

                self.url_number += 1

                if colcnt == 0:
                    outf.write(self.row_start_label())
                    outf.write("\n")
                outf.write(self.col_raw_text(str_url, str_imgf, str_webname, str_descri))
                if colcnt == 3:
                    #outf.write("\n")
                    outf.write(self.row_end_label())
                    outf.write("\n")

                real_line_cnt += 1
                colcnt = (colcnt + 1) % self.ncol

                if self.dbg_row_limit > 0 and dbg_cnt >= self.dbg_row_limit:
                    break
        outf.close()

        tmpname = "mytmp.html"
        with open(outfname, "r", encoding='utf-8') as af:
            line_list = af.readlines()
            output_lines = "\t\t\t".join(line_list)
            output_lines = "\t\t\t" + output_lines
            with open(tmpname, "w", encoding='utf-8') as fw:
                fw.writelines(output_lines)

        os.remove(outfname)
        os.rename(tmpname, outfname)

        print("File line count {} (useful count {})".format(line_cnt, real_line_cnt))
        print("File size =", os.path.getsize(outfname))
        print("End of function generate_body_rows")

        self.body_file = outfname

        return URLMaker.check_file_exists(self.body_file)


    def col_raw_text(self, url, imgf, webname, descri):
        return \
'''    <div class="col-sm-3">
        <div class="xe-widget xe-conversations box2 label-info" onclick="window.open('{}', '_blank')" data-toggle="tooltip" data-placement="bottom" title="" data-original-title="{}">
            <div class="xe-comment-entry">
                <a class="xe-user-img">
                    <img data-src="../assets/images/logos/{}" class="lozad img-circle" width="40">
                </a>
                <div class="xe-comment">
                    <a href="#" class="xe-user-name overflowClip_1">
                        <strong>{}</strong>
                    </a>
                    <p class="overflowClip_2">{}</p>
                </div>
            </div>
        </div>
    </div>
'''.format(url, url, imgf, webname, descri)

    def sidebar_menu_logo_env_raw_test(self, bigimg, smallimg):
        return  '\t\t\t\t<header class="logo-env">\n'\
                '\t\t\t\t\t<!-- logo -->\n'\
                '\t\t\t\t\t<div class="logo">\n'\
                '\t\t\t\t\t\t<a href="index.html" class="logo-expanded">\n'\
                '\t\t\t\t\t\t\t<img src="{}" width="70%" alt="" />\n'\
                '\t\t\t\t\t\t</a>\n'\
                '\t\t\t\t\t\t<a href="index.html" class="logo-collapsed">\n'\
                '\t\t\t\t\t\t\t<img src="{}" width="40" alt="" />\n'\
                '\t\t\t\t\t\t</a>\n'\
                '\t\t\t\t\t</div>\n'\
                '\t\t\t\t\t<div class="mobile-menu-toggle visible-xs">\n'\
                '\t\t\t\t\t\t<a href="#" data-toggle="user-info-menu">\n'\
                '\t\t\t\t\t\t\t<i class="linecons-cog"></i>\n'\
                '\t\t\t\t\t\t</a>\n'\
                '\t\t\t\t\t\t<a href="#" data-toggle="mobile-menu">\n'\
                '\t\t\t\t\t\t\t<i class="fa-bars"></i>\n'\
                '\t\t\t\t\t\t</a>\n'\
                '\t\t\t\t\t</div>\n'\
                '\t\t\t\t</header>\n'.format(bigimg, smallimg)

    def sidebar_menu_raw_test(self, name, icon):
        return '\t\t\t\t\t<li>\n'\
               '\t\t\t\t\t\t<a href="#{}" class="smooth">\n'\
               '\t\t\t\t\t\t\t<i class="{}"></i>\n'\
               '\t\t\t\t\t\t\t<span class="title">{}</span>\n'\
               '\t\t\t\t\t\t</a>\n'\
               '\t\t\t\t\t</li>'.format(name, icon, name)


    def get_sidebar_menu_list(self):
        if self.section_dict is None:
            return

        mlist = []
        for name in self.section_dict.keys():
            # Skip a pseudo section just in case
            if name == "__NOSECTION__":
                continue
            rtext = self.sidebar_menu_raw_test(name, "linecons-star")
            #print(rtext)
            mlist.append(rtext)
        return mlist

    def get_sidebar_main_menu(self):
        tag_start = '\t\t\t\t<ul id = "main-menu" class ="main-menu">'
        tag_end = '\t\t\t\t</ul>\n'
        menulist = self.get_sidebar_menu_list()
        menulist.insert(0, tag_start)
        menulist.append(tag_end)

        for line in menulist:
            print(line)

    def get_section_sets(self):
        # First check if the URL list file exists
        fname = self.url_file
        if not URLMaker.check_file_exists(fname):
            print("Error, file not found:", fname)
            return

        url_pattern = re.compile(r'data-url="(.*)"')
        title_pattern = re.compile(r'title="(.*)"')
        img_pattern = re.compile(r'image="(.*)"')

        # Reset self.section_dict
        self.section_dict = dict()
        self.section_dict['__NOSECTION__'] = []

        line_cnt = 0
        f = open(fname, 'r', encoding='utf-8')

        cur_sect_name = '__NOSECTION__'
        for line in f.readlines():
            line_cnt += 1
            l = line.strip()
            if len(l) == 0:
                continue
            if l.startswith("<!--"):
                llist = l.split()
                if len(llist) == 3:
                    cur_sect_name = llist[1]
                    self.section_dict[cur_sect_name] = []
                continue
            if not l.startswith("data-url"):
                continue

            kwlist = l.split(",")
            assert len(kwlist) == 2 or len(kwlist) == 3

            url_m = url_pattern.match(kwlist[0].strip())
            title_m = title_pattern.match(kwlist[1].strip())
            img_m = img_pattern.match(kwlist[2].strip()) if len(kwlist) == 3 else None

            if url_m is None or title_m is None:
                continue
            str_url = url_m.group(1)
            str_webname = title_m.group(1)
            str_imgf = "undef128x128.png" if img_m is None else img_m.group(1)
            str_imgf = "undef128x128.png" if len(str_imgf) == 0 else str_imgf
            str_descri = str_webname

            csect = self.section_dict[cur_sect_name]
            csect.append([str_url, str_webname, str_imgf, str_descri])

        f.close()

        # for sname, msglist in self.section_dict.items():
        #     print("Section {} has {} items".format(sname, len(msglist)))
        #     for urlstr in msglist:
        #         print("\t", urlstr)

    def generate_index_html(self, fname="index.html", body_file="url.cols.html"):
        if not URLMaker.check_file_exists(self.index_file_head):
            print("[ERROR] The head part (file) for the final index.html doesn't exist")
            return False
        if not URLMaker.check_file_exists(self.index_file_tail):
            print("[ERROR] The tail part (file) for the final index.html doesn't exist")
            return False
        if not self.generate_body_rows(body_file):
            print("[ERROR] Failed to create the body part (file) for the final index.html")
            return False

        self.final_index_html = fname

        with open(fname, "wb") as fout:
            fhead = open(self.index_file_head, "rb")
            fout.write(fhead.read())
            fhead.close()

            fbody = open(self.body_file, "rb")
            fout.write(fbody.read())
            fbody.close()

            # A temp fix to avoid mismatched label
            if self.url_number % 4 != 0:
                fout.write("\t\t\t</div>".encode('utf-8'))

            ftail = open(self.index_file_tail, "rb")
            fout.write(ftail.read())
            ftail.close()

            fout.close()

        if not URLMaker.check_file_exists(fname):
            print("[ERROR] Failed to create the final index.html:", fname)
            return False

        print("File size of {}: {}".format(fname, os.path.getsize(fname)))
        return True

    def do_copy(self, icon_dest, index_html_dest):
        icon_copy_list = []
        icon_missing_list = []
        if len(self.icon_list) == 0:
            print("[ERROR] icon list is empty, skip copy")
            return
        else:
            for icon in self.icon_list:
                iname = "icons/" + icon
                if self.check_file_exists(iname):
                    icon_copy_list.append(icon)
                else:
                    icon_missing_list.append(icon)
            print("[INFO] number of icons to copy is", len(icon_copy_list))
            if len(icon_missing_list) != 0:
                print("[WARNING] Missing following icon files to copy:")
                for icon in icon_missing_list:
                    print("  ", icon)

        if not self.check_file_exists(self.final_index_html):
            print("[ERROR] index file doesn't exist, skip copy")
            return
        if not self.check_dir_exist(icon_dest):
            print("[ERROR] icon_dest directory doesn't exist, skip copy")
            return
        if not self.check_dir_exist(index_html_dest):
            print("[ERROR] index directory doesn't exist, skip copy")
            return

        # Copy index.html file
        src_idx_html = self.final_index_html
        dest_idx_html = index_html_dest + "/" + self.final_index_html
        print("Copying {} to {}".format(src_idx_html, dest_idx_html))
        shutil.copy(src=src_idx_html, dst=dest_idx_html)

        # Copy icon files
        cur_icon_dir = "icons"
        dest_icon_dir = icon_dest
        already_exist_cnt = 0
        for icon in icon_copy_list:
            srcname = cur_icon_dir + "/" + icon
            destname = dest_icon_dir + "/" + icon
            if self.check_file_exists(destname):
                already_exist_cnt += 1
                continue
            shutil.copy(src=srcname, dst=destname)
        if already_exist_cnt != 0:
            print("[WARNING] {} icon already exists in destination directory, skip copy".format(already_exist_cnt))

    @staticmethod
    def default_test():
        url_list_file = "classified_urls.html"
        str_imgf = "undef.png"
        umkr = URLMaker(url_list_file=url_list_file, default_img=str_imgf)

        umkr.get_section_sets()
        umkr.get_sidebar_main_menu()

    @staticmethod
    def default_run():
        url_list_file = "classified_urls.html"
        str_imgf = "undef.png"
        umkr = URLMaker(url_list_file=url_list_file, default_img=str_imgf)

        umkr.generate_index_html("index.html")

        do_copy = True
        #webStackPageDir = "D:/Pyrad/WebHomePage/WebStackPage.github.io-master"
        webStackPageDir = "D:/Programs/TempDownload/WebStackPage.github.io-master/WebStackPage.github.io-master"
        webStackPageDir_snps = "C:/Users/longc/Downloads/WebStackPage.github.io-master"

        use_default_pre = True
        if do_copy:
            path_pre = webStackPageDir if use_default_pre else webStackPageDir_snps
            icon_dest = path_pre + "/assets/images/logos"
            index_html_dest = path_pre + "/cn"
            umkr.do_copy(icon_dest=icon_dest, index_html_dest=index_html_dest)


if __name__ == "__main__":
    #URLMaker.default_run()
    URLMaker.default_test()



