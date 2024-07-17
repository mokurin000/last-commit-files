import os
import subprocess
import zipfile


def get_current_branch():
    result = subprocess.run(
        ["git", "branch", "--show-current"], stdout=subprocess.PIPE, check=False
    )
    return result.stdout.decode("utf-8").strip()


def get_last_commit_files():
    result = subprocess.run(
        ["git", "diff-tree", "--no-commit-id", "--name-only", "-r", "HEAD"],
        stdout=subprocess.PIPE,
        check=False,
    )
    return result.stdout.decode("utf-8").splitlines()


def collect_files(files):
    files_to_add = []
    for file in files:
        if file.endswith(".java"):
            class_file = file.replace(".java", ".class")
            if os.path.exists(class_file):
                files_to_add.append(class_file)
            else:
                print(f"Class file {class_file} not found, skipping.")
        else:
            if os.path.exists(file):
                files_to_add.append(file)
            else:
                print(f"Source file {file} not found, skipping.")
    return files_to_add


def create_zip(files, zip_file_name):
    with zipfile.ZipFile(zip_file_name, "w") as zipf:
        for file in files:
            zipf.write(file)
    print(f"Created zip file: {zip_file_name}")


def main():
    current_branch = get_current_branch()
    print(f"Current branch: {current_branch}")

    if not current_branch:
        print("Not inside a git repository or no current branch.")
        return

    last_commit_files = get_last_commit_files()
    if not last_commit_files:
        print("No files changed in the last commit.")
        return

    files_to_add = collect_files(last_commit_files)
    if not files_to_add:
        print("No files to add to zip.")
        return

    zip_file_name = "files_in_last_commit.zip"
    create_zip(files_to_add, zip_file_name)


if __name__ == "__main__":
    main()
