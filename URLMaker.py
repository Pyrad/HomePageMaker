import re
import os


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
        :return: True if exists, otherwise False
        """
        return True if os.path.exists(fname) else False

    def generate_body_rows(self, outfname="url.cols.html"):
        """
        Generate the main page body which contains the URLs
        :param outfname the file name to write out
        :return: If the outfname is successfully written out
        """

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

                dbg_cnt += 1

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

        with open(fname, "wb") as fout:
            fhead = open(self.index_file_head, "rb")
            fout.write(fhead.read())
            fhead.close()

            fbody = open(self.body_file, "rb")
            fout.write(fbody.read())
            fbody.close()

            ftail = open(self.index_file_tail, "rb")
            fout.write(ftail.read())
            ftail.close()

            fout.close()

        if not URLMaker.check_file_exists(fname):
            print("[ERROR] Failed to create the final index.html:", fname)
            return False

        print("File size of {}: {}".format(fname, os.path.getsize(fname)))
        return True



if __name__ == "__main__":
    url_list_file = "classified_urls.html"
    str_imgf= "undef.png"
    umkr = URLMaker(url_list_file=url_list_file, default_img=str_imgf)

    umkr.generate_index_html("index.html")

