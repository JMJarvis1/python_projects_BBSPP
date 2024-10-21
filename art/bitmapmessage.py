"""
bitmapmessage.py,
maps a user provided message to a bitmap"""

import os
import sys

sys.path.append(os.getcwd() + "/..")

from common_functions import clear_scrn


def main():
    bitmap = """
....................................................................
   **************   *  *** **  *      ******************************
  ********************* ** ** *  * ****************************** *
 **      *****************       ******************************
          *************          **  * **** ** ************** *
           *********            *******   **************** * *
            ********           ***************************  *
   *        * **** ***         *************** ******  ** *
               ****  *         ***************   *** ***  *
                 ******         *************    **   **  *
                 ********        *************    *  ** ***
                   ********         ********          * *** ****
                   *********         ******  *        **** ** * **
                   *********         ****** * *           *** *   *
                     ******          ***** **             *****   *
                     *****            **** *            ********
                    *****             ****              *********
                    ****              **                 *******   *
                    ***                                       *    *
                    **     *                    *
...................................................................."""
    clear_scrn()

    prompt = "Enter a message below, and I'll map it to a bitmap image."
    title = "Bitmap Mesage".center(len(prompt))

    print(title)
    print()
    print(prompt)
    print()

    message = input("> ")

    if message == "":
        sys.exit()

    for line in bitmap.splitlines():
        for index, bit in enumerate(line):
            if bit == " ":
                print(" ", end="")
            else:
                print(message[index % len(message)], end="")
        print()
    print()


if __name__ == "__main__":
    main()
