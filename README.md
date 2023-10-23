This python flashcard program is run on the command line by typing: python flashcards.py

I created it for fun, as I am currently studying Spanish and always have my terminal open when at the computer.

Linux CLI Flashcards uses translate-shell, a separate Linux program for command line translation, which is piped into my program when creating flash cards. Therefore, you will need to ```sudo apt install translate-shell``` first.

It also uses espeak-ng for voice synthesis so we can have audible prompts when studying. Therefore, you will need to do a ```sudo apt install espeak-ng```

Next, please also have mysql installed. 
edit the .env file with your dB credentials.

Next, install the required python libraries 


```
pip install mysql-connector-python
pip install colorama
```

finally, run ```python install.py``` which will initialize the database.

![image](https://github.com/paulpreibisch/linux-cli-flashcards/assets/19810611/d1ed15fa-ada8-4b3a-a032-40706c042cc4)


You can run the program by typing 
```
python flashcards.py
```

