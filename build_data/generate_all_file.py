'''
Author: zyy
Date: 2022-11-15 09:31:37
LastEditTime: 2022-11-15 14:32:06
Description: 
'''
import file_copy
import file_replace
import file_delete
import file_exchange
import file_patch
import file_synthesize

import file_dissim

if __name__ == "__main__":
    file_copy.copy_file()
    file_delete.delete_file()
    file_exchange.exchange_file()
    file_patch.patch_file()
    file_synthesize.synthesize_file()
    file_replace.replace_file()
    file_dissim.dissim_file()