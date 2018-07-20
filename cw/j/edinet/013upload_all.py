from umihico_commons.google_drive import upload_file, get_file_names
import glob
import os
from tqdm import tqdm


def main():
    edinet_doc_folder_id = "1cm7wTRz5co1LlJ1_6sd40f_iYMhrjoqD"
    local_folder_path = "./final/*"
    from time import sleep
    while True:
        local_abs_filenames = [os.path.abspath(p)
                               for p in glob.glob(local_folder_path)]
        local_filenames_dict = {os.path.split(abspath)[1]: os.path.split(abspath)[0]
                                for abspath in local_abs_filenames}
        local_filenames = set(local_filenames_dict.keys())
        gdrive_filenames = set(get_file_names(edinet_doc_folder_id))
        unuploaded_files = local_filenames - gdrive_filenames
        unknownfiles = gdrive_filenames - local_filenames
        if len(unknownfiles) > 1:
            print(unknownfiles)
            raise Exception("something wrong")
        for i, unuploaded_filename in enumerate(unuploaded_files):
            abs_path = os.path.join(
                local_filenames_dict[unuploaded_filename], unuploaded_filename)
            upload_file(abs_path, edinet_doc_folder_id)
            print(abs_path)
            if i > 10:
                break
        else:
            sleep(10)
        sleep(1)


if __name__ == '__main__':
    main()
    # local_folder_path = "./final/*"
    # import os
    # print(glob.glob(local_folder_path, recursive=False))
