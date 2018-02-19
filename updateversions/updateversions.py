import argparse
import re
from io import StringIO
from os import walk
from os.path import join, isdir


# Copyright (c) 2017, 2018 Jason W. Ross
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# Initially described at https://softwarepragmatism.com


class VersionNumberUpdater:

    @staticmethod
    def find_assembly_info_files(root_directory, file_ending='AssemblyInfo.cs'):
        """Iterates through the directory structure starting at the root and searching for files that may contain the
        version definitions for the solution.

        :param root_directory: The root directory of the search. This directory and all of its subdirectories are
        searched for files which may need to be updated.
        :param file_ending: The ending of the file names that will be added to the list of files that should be checked
        for version definitions.
        As most C# projects either contain a file called 'AssemblyInfo.cs', or refer to a common file called
        'CommonAssemblyInfo.cs', this argument defaults to 'AssemblyInfo.cs' to match both names.
        :return: A collection of paths of files which should be checked for version specifications.
        """
        files_to_check = []
        for root, directories, files in walk(root_directory):
            for file_to_check in [filename for filename in files if filename.endswith(file_ending)]:
                files_to_check.append(join(root, file_to_check))

        return files_to_check

    @staticmethod
    def update_version_numbers(file_paths, version_name, build_number):
        """Iterate through all of the given files, updating the version numbers contained within them.

        :param file_paths: A collection of paths of files which are to be checked for version specifications.
        :param version_name: Either 'AssemblyVersion' or 'AssemblyFileVersion' depending upon which of the Windows
        version attributes you want to change.
        :param build_number: The new build number to be placed into the overall version number.
        :return: The paths of the file(s) that were updated.
        """

        version_pattern = '(?P\s*\[assembly\:' + \
                          version_name + \
                          '\(\"\d+\.\d+\.)(?P\d+)(?P\.\d+\"\))'
        version_regex = re.compile(version_pattern)
        updated_file_paths = []

        # Get the contents of each of the files, and update the version numbers.
        for file_path in file_paths:
            version_updated = False

            # Create a memory buffer for the file.
            with StringIO() as buffer_file:

                # Read the source file into memory - there should be plenty of space.
                with open(file_path, mode='r') as file_object:
                    for line_number, line_contents in enumerate(file_object):

                        # Update the version numbers as the file contents are put into the memory file.
                        match = version_regex.match(line_contents)

                        if match:
                            buffer_file.write(
                                version_regex.sub(match.group('prefix') + str(build_number) + match.group('postfix'),
                                                  line_contents))
                            version_updated = True
                        else:
                            buffer_file.write(line_contents)

                # Overwrite the original file with the contents of the memory buffer if the version was updated.
                if version_updated:
                    buffer_file.seek(0)

                    with open(file_path, mode='w') as file_object:
                        file_object.writelines(buffer_file.readlines())

                    updated_file_paths.append(file_path)

        return updated_file_paths


def main():
    """Main function that carries out the updating of files that contain version declarations.

    Copyright 2017,2018 Jason Ross

    :return:
    """

    # Use the argparse module as it produces help automatically.
    parser = argparse.ArgumentParser(description='Update the version number in the source files in the root directory.')

    parser.add_argument('directory',
                        help='The root directory of the search. This directory and all of its subdirectories '
                             'are searched for files which may need to be updated.')
    parser.add_argument('buildnumber', help='The build number to be set in the version declarations.', type=int)
    parser.add_argument('-v', '--versionname',
                        help='The type of version that will be updated by the script. This can be AssemblyVersion (a), '
                             'AssemblyFileVersion(f) or both (b). Default is b.',
                        choices=['a', 'f', 'b'], default='b')
    parser.add_argument('-f', '--fileending',
                        help='The last part of the file to be matched to determine files that may contain version '
                             'data. This is usually ''AssemblyInfo.cs'', but may be ''CommonAssemblyInfo.cs''. '
                             'The default value is ''AssemblyInfo.cs''.',
                        default='AssemblyInfo.cs')

    args = parser.parse_args()

    # Continue only if the directory exists.
    directory_path = args.directory

    if not isdir(directory_path):
        raise NotADirectoryError('The specified directory does not exist: ' + directory_path)

    # Continue only if the build number is valid
    if args.buildnumber < 0:
        raise ValueError('The build number must be larger than or equal to 0. The specified value was: ' +
                         str(args.buildnumber))

    # Set the remaining variables
    version_attribute_name = args.versionname

    # Scan the directories and find the files to check
    if args.fileending is None:
        assembly_info_files = VersionNumberUpdater.find_assembly_info_files(directory_path)
    else:
        assembly_info_files = VersionNumberUpdater.find_assembly_info_files(directory_path, args.fileending)

    # Update the version attributes as required.
    updated_files = []
    if version_attribute_name in ['a', 'b']:
        updated_files.extend(
            VersionNumberUpdater.update_version_numbers(assembly_info_files, 'AssemblyVersion', args.buildnumber))

    if version_attribute_name in ['f', 'b']:
        updated_files.extend(
            VersionNumberUpdater.update_version_numbers(assembly_info_files, 'AssemblyFileVersion', args.buildnumber))

    # Get rid of duplicates - a file may have been updated twice, once for each version type:
    updated_files = sorted(list(set(updated_files)))

    # Let the caller know what was updated
    print('The following files were updated with build number ' + str(args.buildnumber) + ':')
    print('\n'.join(updated_files))
    print('Finished')


main()
