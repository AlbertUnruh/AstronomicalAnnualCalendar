# Astronomical Annual Calendar

This project came about as a small programming idea after I saw a [manually created calendar][aac] ([archive][]) at our observatory.
The manual creation is time-consuming and inaccurate, as average values are used for the sake of simplicity, which is why I wanted to automate the process.

[aac]: https://sternwarte-papenburg.de/jahreskalender/download/ajk_2024.pdf
[archive]: https://web.archive.org/web/20240531110805/https://sternwarte-papenburg.de/jahreskalender/download/ajk_2024.pdf


### But how do I use this project?

The project has been developed as a command line tool. This means that there is no visual interface.

The following must be available on the system:
- Python 3.12+ ([download][Python])
- AstroWin32 *by Dr. Wolfgang Strickling* ([download][AstroWin])

[Python]: https://www.python.org/downloads/
[AstroWin]: https://www.strickling.net/software.htm

Once all programs are available, data must be obtained. AstroWin32 is used for this.


#### Step by step: AstroWin32

1. Activate list calculation </br>
   *button must look "pressed"* </br>
   ![](readme-imgs/AstroWin-1.png)
2. Select date and time </br>
   Example for the year 2024: </br>
   ![](readme-imgs/AstroWin-2.png)
3. Specify observation location </br>
   Example for Papenburg: </br>
   ![](readme-imgs/AstroWin-3.png)
4. Select "Jahrbuchmodus" (yearbook mode) </br>
   *Here is the minimum selection of checkboxes that are required. It is possible to select everything, the data will just not be used* </br>
   ![](readme-imgs/AstroWin-4.png)
5. Then press "Ok" and wait until no more new text appears
6. Click in the text field and press ``strg + A`` (the text should turn blue) and ``strg + C`` </br>
   ![](readme-imgs/AstroWin-6.png)
7. Create and open a new text document in the Explorer
8. Click in the text field and press ``strg + V`` (the text you just copied should appear) and ``strg + S`` </br>
   ![](readme-imgs/AstroWin-8.png)
9. The file is saved and can be closed. **The path will be important in the subsequent steps!**


#### Step by step: AstronomicalAnnualCalendar

1. Download project from [GitHub][] and unpack ZIP </br>
   ![](readme-imgs/AAC-1.png)
2. Navigate to the unzipped folder in Explorer </br>
   *It should look something like this* </br>
   ![](readme-imgs/AAC-2.png)
3. Press ``shift + right-click`` and click on "Open PowerShell window here" (or something like that) </br>
   ![](readme-imgs/AAC-3.png)
4. Enter and execute the desired command to install the dependencies in the command line that has opened, depending on your preference:
   - ``pip install -r requirements.txt``
   - ``poetry install``
     - Poetry version < 2.0.0: execute ``poetry shell`` once
     - Poetry version ≥ 2.0.0: put ``poetry run`` before each ``python ...``
5. An overview of all commands should be visible with the command ``python AstronomicalAnnualCalendar``.
6. The basic command for generating looks like this: ``python AstronomicalAnnualCalendar -l en generate -s text-file -d aac.pdf``.
   - ``-l en`` sets the language to English (could be removed as it's the default)
   - ``text-file`` must be replaced by the path of the text file created earlier
   - ``-d aac.pdf`` saves the result as "aac.pdf"
7. Congratulations! The astronomical annual calendar has been generated! </br>
   *For more details on the command, ``python AstronomicalAnnualCalendar generate --help`` can be executed*

[GitHub]: https://github.com/AlbertUnruh/AstronomicalAnnualCalendar


### Any questions?
Please create an [issue][], I will assist as soon as possible!

[issue]: https://github.com/AlbertUnruh/AstronomicalAnnualCalendar/issues
