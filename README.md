# Independent Signals Article

This repository contains data, scripts, and materials related to the Independent Signals research article. Please follow the instructions below to set up your environment correctly, particularly if you're working on Windows, as some file paths in this repository are quite long.

## Table of Contents
- [Getting Started](#getting-started)
- [Long Path Support](#long-path-support)
- [Git Setup for Long Paths](#git-setup-for-long-paths)
- [Cloning the Repository](#cloning-the-repository)
- [Contributing](#contributing)

## Getting Started

To work with this repository, follow the steps below:

1. Ensure you have [Git](https://git-scm.com/) installed.
2. If you are using **Windows**, configure your system for long file path support (see the next section).
3. Clone the repository following the instructions below.

## Long Path Support

### Windows Users:
Windows has a default limit of 260 characters for file paths, which may cause issues when working with some files in this repository. To avoid problems, you need to enable long path support on your system.

#### Enable Long Path Support in Windows 10/11:
1. **For Windows 10 Pro, Enterprise, or Education**:
   - Open **Group Policy Editor** by pressing `Win + R`, typing `gpedit.msc`, and pressing Enter.
   - Navigate to `Local Computer Policy > Computer Configuration > Administrative Templates > System > Filesystem`.
   - Double-click the `Enable Win32 long paths` option.
   - Set it to **Enabled** and click **OK**.

2. **For Windows 10 Home**:
   - Open **Registry Editor** by pressing `Win + R`, typing `regedit`, and pressing Enter.
   - Navigate to:  
     `HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\FileSystem`.
   - Right-click and create a new `DWORD (32-bit) Value` called `LongPathsEnabled`.
   - Set the value of `LongPathsEnabled` to `1`.
   - Restart your computer for the changes to take effect.

## Git Setup for Long Paths

After enabling long path support in Windows, you need to tell Git to handle long file paths. To do this:

1. Open a terminal or command prompt in the root directory of this repository.
2. Run the following command to enable long path support for this repository:

   ```bash
   git config core.longpaths true
