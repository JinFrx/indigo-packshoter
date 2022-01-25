# Indigo Packshoter

<p align=center>
  <img src="https://github.com/JinFrx/indigo-packshoter/blob/main/showcase.PNG" alt="showcase image" style="width: 650px; max-width: 100%; height: auto" title="Click to enlarge picture" />
</p>

## Description

A simple graphical tool in Python 3.9 for Indigo Renderer engine made as part of a university project (2022).

The main goal of such project was to make, along with a proper notice, a utility for Indigo Renderer which allows to create packshots of a Indigo scene from a Indigo materials database.

This tool enables the user to assign different materials from a local database (.igm files) to an Indigo object (.igs file), and to assign a Indigo camera (.igs file) to a Indigo scene (.igs file), in order to generate a packshot by launching a render through a subprocess that calls the Indigo Renderer console executable.

The project support a notice, where the main aspects of the utility are detailed, for the assumed user and for the assumed developer.

The executable was generated with "pyinstaller". Source code is located in the directory "src", at the root of the project.

## Dev Note

Because the tool was made for the purpose of university work and because there is no interest for me to continue the project, no proper redesign or update are planned at the moment.
