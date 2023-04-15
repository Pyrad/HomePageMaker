import re
import os
import shutil
import uuid
from colorama import init as clma_init
from colorama import Fore as clma_Fore
from colorama import Back as clma_Back
from getmac import get_mac_address as gma

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

    def print_error(self, errmsgstr):
        print(clma_Back.RED + '[ ERROR ]', end="")
        print('', errmsgstr)

    def print_info(self, infomsgstr):
        print(clma_Back.GREEN + '[  INFO ]', end="")
        print('', infomsgstr)

    def print_warning(self, warnmsgstr):
        print(clma_Back.LIGHTYELLOW_EX + '[WARNING]', end="")
        print('', warnmsgstr)

    def get_page_head_raw_text(self):
        return  '<head>\n'\
                '\t<meta charset="utf-8">\n'\
                '\t<meta http-equiv="X-UA-Compatible" content="IE=edge">\n'\
                '\t<meta name="viewport" content="width=device-width, initial-scale=1.0" />\n'\
                '\t<meta name="author" content="viggo" />\n'\
                '\t<title>Pyrad Home</title>\n'\
                '\t<meta name="keywords" content="Site Navigation Main Page - keywords">\n'\
                '\t<meta name="description" content="Site Navigation Main Page - description">\n'\
                '\t<link rel="shortcut icon" href="../assets/images/favicon.png">\n'\
                '\t<link rel="stylesheet" href="http://fonts.googleapis.com/css?family=Arimo:400,700,400italic">\n'\
                '\t<link rel="stylesheet" href="../assets/css/fonts/linecons/css/linecons.css">\n'\
                '\t<link rel="stylesheet" href="../assets/css/fonts/fontawesome/css/font-awesome.min.css">\n'\
                '\t<link rel="stylesheet" href="../assets/css/bootstrap.css">\n'\
                '\t<link rel="stylesheet" href="../assets/css/xenon-core.css">\n'\
                '\t<link rel="stylesheet" href="../assets/css/xenon-components.css">\n'\
                '\t<link rel="stylesheet" href="../assets/css/xenon-skins.css">\n'\
                '\t<link rel="stylesheet" href="../assets/css/nav.css">\n'\
                '\t<script src="../assets/js/jquery-1.11.1.min.js"></script>\n'\
                '\t<!-- HTML5 shim and Respond.js IE8 support of HTML5 elements and media queries -->\n'\
                '\t<!--[if lt IE 9]>\n'\
                '\t\t<script src="https://oss.maxcdn.com/html5shiv/3.7.2/html5shiv.min.js"></script>\n'\
                '\t\t<script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>\n'\
                '\t<![endif]-->\n'\
                '\t<!-- / FB Open Graph -->\n'\
                '\t<meta property="og:type" content="article">\n'\
                '\t<meta property="og:url" content="http://www.webstack.cc/">\n'\
                '\t<meta property="og:title" content="Site Navigation og:title">\n'\
                '\t<meta property="og:description" content="Site Navigation og:description">\n'\
                '\t<meta property="og:image" content="http://webstack.cc/assets/images/webstack_banner_cn.png">\n'\
                '\t<meta property="og:site_name" content="Site Navigation og:site_name">\n'\
                '\t<!-- / Twitter Cards -->\n'\
                '\t<meta name="twitter:card" content="summary_large_image">\n'\
                '\t<meta name="twitter:title" content="Site Navigation twitter:title">\n'\
                '\t<meta name="twitter:description" content="Site Navigation twitter:description">\n'\
                '\t<meta name="twitter:image" content="http://www.webstack.cc/assets/images/webstack_banner_cn.png">\n'\
                '</head>'

    def get_page_body_script_raw_text(self):
        return  '\t<!-- 锚点平滑移动 -->\n'\
                '\t<script type="text/javascript">\n'\
                '\t$(document).ready(function() {\n'\
                '\t\t//img lazy loaded\n'\
                '\t\tconst observer = lozad();\n'\
                '\t\tobserver.observe();\n'\
                '\t\t$(document).on(\'click\', \'.has-sub\', function(){\n'\
                '\t\t\tvar _this = $(this)\n'\
                '\t\t\tif(!$(this).hasClass(\'expanded\')) {\n'\
                '\t\t\t\tsetTimeout(function(){_this.find(\'ul\').attr("style","")}, 300);\n'\
                '\t\t\t} else {\n'\
                '\t\t\t\t$(\'.has-sub ul\').each(function(id,ele){\n'\
                '\t\t\t\t\tvar _that = $(this)\n'\
                '\t\t\t\t\tif(_this.find(\'ul\')[0] != ele) {\n'\
                '\t\t\t\t\t\tsetTimeout(function(){_that.attr("style","")}, 300);\n'\
                '\t\t\t\t\t}\n'\
                '\t\t\t\t})\n'\
                '\t\t\t}\n'\
                '\t\t})\n'\
                '\t\t$(\'.user-info-menu .hidden-sm\').click(function(){\n'\
                '\t\t\tif($(\'.sidebar-menu\').hasClass(\'collapsed\')) {\n'\
                '\t\t\t\t$(\'.has-sub.expanded > ul\').attr("style","")\n'\
                '\t\t\t} else {\n'\
                '\t\t\t\t$(\'.has-sub.expanded > ul\').show()\n'\
                '\t\t\t}\n'\
                '\t\t})\n'\
                '\t\t$("#main-menu li ul li").click(function() {\n'\
                '\t\t\t$(this).siblings(\'li\').removeClass(\'active\'); // 删除其他兄弟元素的样式\n'\
                '\t\t\t$(this).addClass(\'active\'); // 添加当前元素的样式\n'\
                '\t\t});\n'\
                '\t\t$("a.smooth").click(function(ev) {\n'\
                '\t\t\tev.preventDefault();\n'\
                '\t\t\tpublic_vars.$mainMenu.add(public_vars.$sidebarProfile).toggleClass(\'mobile-is-visible\');\n'\
                '\t\t\tps_destroy();\n'\
                '\t\t\t$("html, body").animate({\n'\
                '\t\t\t\tscrollTop: $($(this).attr("href")).offset().top - 30\n'\
                '\t\t\t}, {\n'\
                '\t\t\t\tduration: 500,\n'\
                '\t\t\t\teasing: "swing"\n'\
                '\t\t\t});\n'\
                '\t\t});\n'\
                '\t\treturn false;\n'\
                '\t});\n'\
                '\t\n'\
                '\tvar href = "";\n'\
                '\tvar pos = 0;\n'\
                '\t$("a.smooth").click(function(e) {\n'\
                '\t\t$("#main-menu li").each(function() {\n'\
                '\t\t\t$(this).removeClass("active");\n'\
                '\t\t});\n'\
                '\t\t$(this).parent("li").addClass("active");\n'\
                '\t\te.preventDefault();\n'\
                '\t\thref = $(this).attr("href");\n'\
                '\t\tpos = $(href).position().top - 30;\n'\
                '\t});\n'\
                '\t</script>\n'\
                '\t<!-- Bottom Scripts -->\n'\
                '\t<script src="../assets/js/bootstrap.min.js"></script>\n'\
                '\t<script src="../assets/js/TweenMax.min.js"></script>\n'\
                '\t<script src="../assets/js/resizeable.js"></script>\n'\
                '\t<script src="../assets/js/joinable.js"></script>\n'\
                '\t<script src="../assets/js/xenon-api.js"></script>\n'\
                '\t<script src="../assets/js/xenon-toggles.js"></script>\n'\
                '\t<!-- JavaScripts initializations and stuff -->\n'\
                '\t<script src="../assets/js/xenon-custom.js"></script>\n'\
                '\t<script src="../assets/js/lozad.js"></script>\n'


    def get_col_raw_text(self, url, imgf, webname, descri):
        return  '\t\t\t\t<div class="col-sm-3">\n'\
                '\t\t\t\t\t<div class="xe-widget xe-conversations box2 label-info" onclick="window.open(\'{}\', \'_blank\')" data-toggle="tooltip" data-placement="bottom" title="" data-original-title="{}">\n'\
                '\t\t\t\t\t\t<div class="xe-comment-entry">\n'\
                '\t\t\t\t\t\t\t<a class="xe-user-img">\n'\
                '\t\t\t\t\t\t\t\t<img data-src="../assets/images/logos/{}" class="lozad img-circle" width="40">\n'\
                '\t\t\t\t\t\t\t</a>\n'\
                '\t\t\t\t\t\t\t<div class="xe-comment">\n'\
                '\t\t\t\t\t\t\t\t<a href="#" class="xe-user-name overflowClip_1">\n'\
                '\t\t\t\t\t\t\t\t\t<strong>{}</strong>\n'\
                '\t\t\t\t\t\t\t\t</a>\n'\
                '\t\t\t\t\t\t\t\t<p class="overflowClip_2">{}</p>\n'\
                '\t\t\t\t\t\t\t</div>\n'\
                '\t\t\t\t\t\t</div>\n'\
                '\t\t\t\t\t</div>\n'\
                '\t\t\t\t</div>'.format(url, url, imgf, webname, descri)

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
                '\t\t\t\t</header>'.format(bigimg, smallimg)

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

        # for line in menulist:
        #     print(line)

        return menulist

    def get_side_bar_menu_inner(self, biglogo, smalllogo):
        tag_start = '\t\t\t<div class="sidebar-menu-inner">'
        tag_end = '\t\t\t</div>'
        logo_part_lines = self.sidebar_menu_logo_env_raw_test(bigimg=biglogo, smallimg=smalllogo)
        sidebar_main_menu_lines = self.get_sidebar_main_menu()
        inner_lines = [tag_start, logo_part_lines]
        inner_lines.extend(sidebar_main_menu_lines)
        inner_lines.append(tag_end)
        return inner_lines


    def get_side_bar_menu(self, biglogo, smalllogo):
        tag_start = '\t\t<div class ="sidebar-menu toggle-others fixed">'
        tag_end = '\t\t</div>'
        mlist = self.get_side_bar_menu_inner(biglogo=biglogo, smalllogo=smalllogo)
        mlist.insert(0, tag_start)
        mlist.append(tag_end)

        #for line in mlist:
        #    print(line)

        return mlist

    def get_navbar_raw_text(self):
        return  '\t\t\t<nav class="navbar user-info-navbar" role="navigation">\n'\
                '\t\t\t\t<!-- User Info, Notifications and Menu Bar -->\n'\
                '\t\t\t\t<!-- Left links for user info navbar -->\n'\
                '\t\t\t\t<ul class="user-info-menu left-links list-inline list-unstyled">\n'\
                '\t\t\t\t\t<li class="hidden-sm hidden-xs">\n'\
                '\t\t\t\t\t\t<a href="#" data-toggle="sidebar">\n'\
                '\t\t\t\t\t\t\t<i class="fa-bars"></i>\n'\
                '\t\t\t\t\t\t</a>\n'\
                '\t\t\t\t\t</li>\n'\
                '\t\t\t\t\t<li class="dropdown hover-line language-switcher">\n'\
                '\t\t\t\t\t\t<a href="../cn/index.html" class="dropdown-toggle" data-toggle="dropdown">\n'\
                '\t\t\t\t\t\t\t<img src="../assets/images/flags/flag-cn.png" alt="flag-cn" /> Chinese\n'\
                '\t\t\t\t\t\t</a>\n' \
                '\t\t\t\t\t\t<ul class="dropdown-menu languages">\n' \
                '\t\t\t\t\t\t\t<li>\n' \
                '\t\t\t\t\t\t\t\t<a href="../en/index.html">\n' \
                '\t\t\t\t\t\t\t\t\t<img src="../assets/images/flags/flag-us.png" alt="flag-us" /> English\n' \
                '\t\t\t\t\t\t\t\t</a>\n' \
                '\t\t\t\t\t\t\t</li>\n' \
                '\t\t\t\t\t\t\t<li class="active">\n' \
                '\t\t\t\t\t\t\t\t<a href="../cn/index.html">\n' \
                '\t\t\t\t\t\t\t\t\t<img src="../assets/images/flags/flag-cn.png" alt="flag-cn" /> Chinese\n' \
                '\t\t\t\t\t\t\t\t</a>\n' \
                '\t\t\t\t\t\t\t</li>\n' \
                '\t\t\t\t\t\t</ul>\n' \
                '\t\t\t\t\t</li>\n' \
                '\t\t\t\t</ul>\n' \
                '\t\t\t\t<ul class="user-info-menu right-links list-inline list-unstyled">\n' \
                '\t\t\t\t\t<li class="hidden-sm hidden-xs">\n' \
                '\t\t\t\t\t\t<a href="https://github.com/WebStackPage/WebStackPage.github.io" target="_blank">\n' \
                '\t\t\t\t\t\t\t<i class="fa-github"></i>  GitHub\n' \
                '\t\t\t\t\t\t</a>\n' \
                '\t\t\t\t\t</li>\n' \
                '\t\t\t\t</ul>\n' \
                '\t\t\t\t<!-- <a href="https://github.com/WebStackPage/WebStackPage.github.io" target="_blank"><img style="position: absolute; top: 0; right: 0; border: 0;" src="https://s3.amazonaws.com/github/ribbons/forkme_right_darkblue_121621.png" alt="Fork me on GitHub"></a> -->\n' \
                '\t\t\t</nav>'

    def get_category_tag_line(self, catname):
        return '\t\t\t<h4 class="text-gray"><i class="linecons-tag" style="margin-right: 7px;" id="{}"></i>{}</h4>'.format(catname, catname)

    def get_all_section_rows(self):
        allsectlines = []
        for category_name, urllist in self.section_dict.items():
            if category_name == "__NOSECTION__":
                continue
            tagline = self.get_category_tag_line(catname=category_name)
            allsectlines.append(tagline)
            colcnt = 0
            cnt = 0
            urllistlen = len(urllist)
            for item in urllist:
                if colcnt == 0:
                    allsectlines.append('\t\t\t<div class="row">')
                str_url, str_webname, str_imgf, str_descri = item[0], item[1], item[2], item[3]
                cur_col_line = self.get_col_raw_text(url=str_url, imgf=str_imgf, webname=str_webname, descri=str_descri)
                allsectlines.append(cur_col_line)
                if colcnt == 3 or cnt == urllistlen - 1:
                    allsectlines.append('\t\t\t</div>')

                colcnt = (colcnt + 1) % 4
                cnt += 1
            allsectlines.append('\t\t\t<br />')

        #for sline in allsectlines:
        #    print(sline)
        return allsectlines

    def get_main_footer(self, yearBegin, yearEnd, designName, authorLink, authorName):
        return  '\t\t\t<!-- Main Footer -->\n'\
                '\t\t\t<!-- Choose between footer styles: "footer-type-1" or "footer-type-2" -->\n'\
                '\t\t\t<!-- Add class "sticky" to  always stick the footer to the end of page (if page contents is small) -->\n'\
                '\t\t\t<!-- Or class "fixed" to  always fix the footer to the end of page -->\n'\
                '\t\t\t<footer class="main-footer sticky footer-type-1">\n'\
                '\t\t\t\t<div class="footer-inner">\n'\
                '\t\t\t\t\t<!-- Add your copyright text here -->\n'\
                '\t\t\t\t\t<div class="footer-text">\n'\
                '\t\t\t\t\t\t&copy; {}-{}\n'\
                '\t\t\t\t\t\t<a href="../cn/about.html"><strong>{}</strong></a> design by <a href="{}" target="_blank"><strong>{}</strong></a>\n'\
                '\t\t\t\t\t\t<!--  - Purchase for only <strong>23$</strong> -->\n'\
                '\t\t\t\t\t</div>\n'\
                '\t\t\t\t\t<!-- Go to Top Link, just add rel="go-top" to any link to add this functionality -->\n'\
                '\t\t\t\t\t<div class="go-up">\n'\
                '\t\t\t\t\t\t<a href="#" rel="go-top">\n'\
                '\t\t\t\t\t\t\t<i class="fa-angle-up"></i>\n'\
                '\t\t\t\t\t\t</a>\n'\
                '\t\t\t\t\t</div>\n'\
                '\t\t\t\t</div>\n'\
                '\t\t\t</footer>'.format(yearBegin, yearEnd, designName, authorLink, authorName)

    def get_main_content(self):
        main_content_lines = []
        tag_start = '\t\t<div class="main-content">'
        tag_end = '\t\t</div>'

        yearBegin, yearEnd = 2021, 2022
        designName, authorName = 'LifeTour', 'Pyrad'
        authorLink = 'https://pyrad.github.io/'

        main_content_lines.append(tag_start)
        main_content_lines.append(self.get_navbar_raw_text())
        main_content_lines.extend(self.get_all_section_rows())
        main_content_lines.append(self.get_main_footer(yearBegin, yearEnd, designName, authorLink, authorName))
        main_content_lines.append(tag_end)

        return main_content_lines

    def get_page_container(self, biglogo, smalllogo):
        slines = ['\t<!-- skin-white -->', '\t<div class ="page-container" >']
        slines.extend(self.get_side_bar_menu(biglogo=biglogo, smalllogo=smalllogo))
        slines.extend(self.get_main_content())
        slines.append('\t</div>')

        return slines

    def get_page_body(self, biglogo, smalllogo):
        slines = ['<body class="page-body">']
        slines.extend(self.get_page_container(biglogo=biglogo, smalllogo=smalllogo))
        slines.append(self.get_page_body_script_raw_text())
        slines.append('</body>')

        return slines

    def get_index_html(self, biglogo, smalllogo):
        slines = ['<!DOCTYPE html>', '<html lang="zh">']
        slines.append(self.get_page_head_raw_text())
        slines.extend(self.get_page_body(biglogo=biglogo, smalllogo=smalllogo))
        slines.append('</html>')

        return slines

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

    def do_copy(self, icon_dest, index_html_dest):
        # Copy icon images
        # First get all the icon images list (represented by a set)
        all_icon_list = []
        for category_name, urllist in self.section_dict.items():
            if category_name == "__NOSECTION__":
                continue
            all_icon_list.extend([item[2] for item in urllist])
        all_icon_set = set(all_icon_list)

        icon_copy_list = []
        icon_missing_list = []
        if len(all_icon_set) == 0:
            self.print_error("icon list is empty, skip copy")
            return
        else:
            for icon in all_icon_set:
                iname = "icons/" + icon
                if self.check_file_exists(iname):
                    icon_copy_list.append(icon)
                else:
                    icon_missing_list.append(icon)
            self.print_info("number of icons to copy is {}".format(len(icon_copy_list)))
            if len(icon_missing_list) != 0:
                self.print_warning("Missing following icon files ({} in total) to copy:".format(len(icon_missing_list)))
                for icon in icon_missing_list:
                    print("  ", icon)

        if not self.check_file_exists(self.final_index_html):
            self.print_error("index file doesn't exist, skip copy")
            return
        if not self.check_dir_exist(icon_dest):
            self.print_error("icon_dest directory doesn't exist, skip copy")
            self.print_error("  icon_dest directory is {}".format(icon_dest))
            return
        if not self.check_dir_exist(index_html_dest):
            self.print_error("index directory doesn't exist, skip copy")
            return

        # Copy index.html file
        src_idx_html = self.final_index_html
        dest_idx_html = index_html_dest + "/" + self.final_index_html
        self.print_info("Copying {} to {}".format(src_idx_html, dest_idx_html))
        shutil.copy(src=src_idx_html, dst=dest_idx_html)

        # Copy icon files
        cur_icon_dir = "icons"
        dest_icon_dir = icon_dest
        already_exist_cnt = 0
        copy_cnt = 0
        for icon in icon_copy_list:
            srcname = cur_icon_dir + "/" + icon
            destname = dest_icon_dir + "/" + icon
            if self.check_file_exists(destname):
                already_exist_cnt += 1
                continue
            shutil.copy(src=srcname, dst=destname)
            copy_cnt += 1
        if already_exist_cnt != 0:
            self.print_warning("{} icons already exists in destination directory, skip copy".format(already_exist_cnt))
        self.print_info("Copied {} icons".format(copy_cnt))

    def get_data_dir_on_this_computer_by_mac_address(self):
        MyPCMacStr = '0x502b73d0046d'
        MyLenovoMacStr = '0x1063c8d8c61f'
        MySnpsMacStr = '0xf4ee08c054fe'
        MySnpsMacStrWiFi = '0x7c70db2df05e'
        # Looks uuid.getnode() sometimes return an invalid number
        # Still don't know why, so use get_mac module instead
        # 2023-04-15
        #current_mac_str = hex(uuid.getnode())
        current_mac_str = hex(int(gma().replace(':', ''), 16))

        webStackPageDir = None
        if current_mac_str == MyPCMacStr:
            # If current PC is my ASUS computer
            webStackPageDir = "D:/Programs/TempDownload/WebStackPage.github.io-master/WebStackPage.github.io-master"
        elif current_mac_str == MyLenovoMacStr:
            webStackPageDir = "D:/Pyrad/WebHomePage/WebStackPage.github.io-master"
        elif current_mac_str == MySnpsMacStr or current_mac_str == MySnpsMacStrWiFi:
            # If current PC is my work computer from SNSP
            webStackPageDir = "C:/Users/longc/Downloads/WebStackPage.github.io-master"
        else:
            self.print_error("Can't identify the mac address ({}) for this PC, please verify.".format(current_mac_str))

        return webStackPageDir, current_mac_str

    @staticmethod
    def default_test():
        clma_init(autoreset=True)

        url_list_file = "classified_urls.html"
        str_imgf = "undef.png"
        umkr = URLMaker(url_list_file=url_list_file, default_img=str_imgf)

        logo_big = "../assets/images/worldwide.png"
        logo_small = "../assets/images/globe64.png"

        umkr.get_section_sets()

        #testdir = 'F:/Pyrad/tmps'
        #sline_file = 'sline_tmp.html'
        #sline_file = 'index.html'
        #fname = testdir + '/' + sline_file
        fname = 'index.html'

        slines = umkr.get_index_html(biglogo=logo_big, smalllogo=logo_small)

        output_lines = "\n".join(slines)
        with open(fname, "w", encoding='utf-8') as fw:
            fw.writelines(output_lines)

        copyIndexIcons = True

        webStackPageDir, current_mac_str = umkr.get_data_dir_on_this_computer_by_mac_address()
        if webStackPageDir is None:
            raise ValueError(f"Invalid mac address found: {current_mac_str}")

        umkr.final_index_html = "index.html"

        if copyIndexIcons is True:
            icon_dest = webStackPageDir + "/assets/images/logos"
            index_html_dest = webStackPageDir + "/cn"
            umkr.do_copy(icon_dest=icon_dest, index_html_dest=index_html_dest)


if __name__ == "__main__":
    URLMaker.default_test()



