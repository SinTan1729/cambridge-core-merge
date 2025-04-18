#!/usr/bin/env python

# SPDX-FileCopyrightText: 2025 Sayantan Santra <sayantan.santra689@gmail.com>
# SPDX-License-Identifier: GPL-3.0-only

from pypdf import PdfWriter, PdfReader
from zipfile import ZipFile
from argparse import ArgumentParser
from roman import fromRoman
from PIL import Image
from tempfile import TemporaryFile


def main():
    parser = ArgumentParser(
        prog="cambridge-core-merge",
        description="A python script to merge books downloaded from Cambridge Core into a single PDF file",
        epilog="Copyright (C) 2025  Sayantan Santra",
    )
    parser.add_argument(
        "-z",
        "--zipfile",
        required=True,
        help="The path of the zip file obtained from Cambridge Core.",
    )
    parser.add_argument("-n", "--name", required=True, help="The path of the final PDF file.")
    parser.add_argument("-c", "--cover", help="The path of the cover file. (Must be JPG.)")
    args = parser.parse_args()

    zip = ZipFile(args.zipfile, "r")
    filelist = zip.namelist()
    filelist.sort()

    merger = PdfWriter()
    first_bookmark = True
    for file in filelist:
        print("Adding " + file)
        parts = file.split("_", 4)
        # This is just using how the naming scheme works for these files from Cambridge Core
        name = parts[4][:-4].replace("_", " ")
        start_index = merger.get_num_pages()

        with zip.open(file) as pdf:
            merger.append(pdf)
        # Need to do this here for keeping proper order of the bookmarks
        if first_bookmark and args.cover is not None:
            cover = Image.open(args.cover, "r")
            h = merger.pages[0].mediabox.height
            w = merger.pages[0].mediabox.width
            # Note: UserUnit is 1/72 inch by default and our target dpi is 300
            h = int(h * 300 / 72)
            w = int(w * 300 / 72)
            cover = cover.resize([w, h])
            temp = TemporaryFile()
            cover.save(temp, "PDF", dpi=[300, 300])
            merger.insert_page(PdfReader(temp).get_page(0), 0)
            merger.add_outline_item("Cover", 0)
            start_index += 1
            # I know, this is a weird hack, r is the 18th letter in the alphabet lol
            merger.set_page_label(0, 0, "/a", prefix="cove", start=18)
            first_bookmark = False
            temp.close()
        merger.add_outline_item(name, start_index)

        startpage_str = parts[2]
        endpage_str = parts[3]
        # '/D' means the decimal numbers
        pagestyle = "/D"
        startpage, endpage = None, None
        try:
            startpage = int(startpage_str)
            endpage = int(endpage_str)
        except ValueError:
            # '/r' means the roman numbers
            pagestyle = "/r"
            startpage = fromRoman(startpage_str)
            endpage = fromRoman(endpage_str)
        merger.set_page_label(
            start_index,
            start_index + endpage - startpage,
            style=pagestyle,
            start=startpage,
        )

    merger.write(args.name + ".pdf")
    merger.close()


if __name__ == "__main__":
    main()
