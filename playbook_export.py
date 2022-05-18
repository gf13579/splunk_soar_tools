from os import listdir
import os
import fnmatch
from os.path import isfile, join
from loguru import logger
import shutil


class PlaybookExport:
    def __init__(self):
        pass

    def copy_pb_directory(self, path: str, dest_folder: str):
        shutil.copytree(path, dest_folder)

    def change_repo_names(self, path: str, old_repo: str, new_repo: str):
        files = [f for f in listdir(path) if isfile(join(path, f))]

        for filename in files:
            file_path = f"{path}/{filename}"
            # if py or json, replace repo_name/ (note trailing slash)
            if filename.endswith(".py") or filename.endswith(".json"):
                os.system(f"sed -i 's/{old_repo}\//{new_repo}\//g' '{file_path}'")
            # if json, replace when our repo name is referenced in the repoName field
            elif filename.endswith(".json"):
                os.system(
                    f'sed -i \'s/"repoName": "{old_repo}"/"repoName": "{new_repo}"/g\' "{file_path}"'
                )
        # cf_path = path + "/custom_functions"
        # cf_files = [f for f in listdir(cf_path) if isfile(join(cf_path, f))]

    def change_asset_names(self, path: str, old_asset_name: str, new_asset_name: str):
        files = [f for f in listdir(path) if isfile(join(path, f))]

        for filename in files:
            file_path = f"{path}/{filename}"
            # if py or json, replace "asset_name" (note the quotes)
            if filename.endswith(".py") or filename.endswith(".json"):
                os.system(
                    f"sed -i 's/\"{old_asset_name}\"/\"{new_asset_name}\"/g' '{file_path}'"
                )

    def export_pbs_as_tgz(self, path: str):

        os.mkdir(os.path.join(path, "tgz"))

        json_files = fnmatch.filter(
            [f for f in listdir(path) if isfile(join(path, f))], "*.json"
        )
        for json_file in json_files:
            file_stem = os.path.splitext(f"{json_file}")[0]
            path_stem = f"{path}/tgz/{file_stem}"
            command = f"tar -C {path} -cvzf '{path_stem}.tgz' '{file_stem}.py' '{file_stem}.json'"
            # logger.debug(command)
            os.system(command)


if __name__ == "__main__":
    pbe = PlaybookExport()
    dest_folder = "/tmp/pb-exported"
    shutil.rmtree(dest_folder, ignore_errors=True)
    pbe.copy_pb_directory(
        path="/opt/soar/scm/git/gf-phantom-dev", dest_folder=dest_folder
    )

    pbe.change_repo_names(path=dest_folder, old_repo="gf-phantom-dev", new_repo="local")
    # pbe.change_asset_names(path=dest_folder, old_asset_name="splunk_http", new_asset_name="dirty_http")

    pbe.export_pbs_as_tgz(path=dest_folder)
