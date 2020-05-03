# TA-Mentor kit for LMS platform

## Features
* Submission file filtering
* Submission file runner
    - `.py`
    - `.c` (only on Linux, with `gcc`)
* Result viewer

## Requirements
* Python 3 (tested on Python 3.5+)
* `pip`
* `gcc` (for `.c` files)

* Supported submission file format: `[NAME-ID]FILENAME.EXTENSION`
    - Example: `[Percy Jackson-20209876]hello_world.c`

## Instructions

1. Clone repository and enter the project directory.
    ```bash
    git clone https://github.com/hummingbird-12/mentor-kit
    cd mentor-kit
    ```
2. Start `venv` and install dependencies.
    * Linux
        ```bash
        cd venv/Scripts
        source activate
        # Notice that `(venv)` has been added in front of the input prompt
        pip3 install -r ../../requiremetns.txt 
        cd ../../
        ```
    * Windows
        ```bash
        cd venv\Scripts
        activate.bat
        # Notice that `(venv)` has been added in front of the input prompt
        pip3 install -r ..\..\requiremetns.txt 
        cd ..\..\
        ```
3. Add students' (or mentees') into `mentee.csv` file.
    > Check out `mentee.csv.example` file for an example.
4. Create the `submissions` directory and add submission files in it.
5. Run the program.
    * Linux
        ```bash
        python3 main.py
        ```
    * Windows
        ```bash
        python main.py
        ```
6. After evaluation is complete, deactivate `venv`.
    ```bash
    deactivate
    ```
7. The evaluation result is printed on screen and also available in `result.csv`. 

## Developer
Inho Kim
