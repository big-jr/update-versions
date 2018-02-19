# update-versions
Update the build numbers in .NET source files. Ideal for part of a continuous integration / build system.

## Summary
This Python 3 script allows you to update the build number in the version settings in C# .NET source files. It can be run from the command prompt or from within a build system and will set the build numbers in the `AssemblyInfo.cs` or `CommonAssemblyInfo.cs` files in a given directory and its subdirectories.
## Details
If you're using an automated build / continuous integration (CI) system, you probably want to update the version numbers of the files being built as part of the build process.

One way to implement automatic versioning in your build system could be:

- Obtain the current build number. This is something that the build server (certainly Jenkins and TeamCity) will provide easily, usually as a macro or variable that you can use in command lines or scripts.
- Update the version number in your source code. Ideally this would be in one place, but it may be in several especially if you’re developing in several languages.
- Carry out the build for your system
To simplify things, if you’re using C# and you have a solution comprising multiple projects, you could remove the common information from all of the `AssemblyInfo.cs` files (Company details, copyright, version specifications etc.) and place it in a new file called `CommonAssemblyInfo.cs` in the root folder with the solution. Add this file to each project as a link, **NOT** a source file. Once you’ve done this, any changes to `CommonAssemblyInfo.cs` will naturally appear in all of the modules.
## Version Numbering
[MSDN Article: Assembly Versioning - The Significance Of Each Of The Numbers In A Version](https://docs.microsoft.com/en-ca/dotnet/framework/app-domains/assembly-versioning) says that the structure of the Windows version block is:
```
<major version><minor version><build number><revision>
```
There are two version numbers in .NET, AssemblyVersion and AssemblyFileVersion. The differences between them are explained at: [MSDN Article: How to use Assembly Version and Assembly File Version](https://support.microsoft.com/en-ca/help/556041).
Alternatively for APIs the [SemVer2 standard](https://semver.org) is straightforward, logical and has helped at least one of my friends’ departments pass a development audit. It’s definitely worth considering.
## Using The Script
From a Windows command line, if you want to set the versions in the files in the directory `E:\Articles\Examples\Versioning` to 7434 this script can be run as:
```
python updateversions.py "E:\Articles\Examples\Versioning" 7434
```
Running:
```
python updateversions.py -h
```
will display the required and optional parameters for the script.
## Unit Tests
This script has no unit tests at the moment. A future version will probably include tests.
## Licence
This project is licensed under the terms of the MIT license.
## References
The original version of this script was published as part of my web site at:
[https://softwarepragmatism.com/automatically-version-everything](https://softwarepragmatism.com/automatically-version-everything)
