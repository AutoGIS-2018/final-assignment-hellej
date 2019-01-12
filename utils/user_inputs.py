def get_user_input(text, options, caseSens, error):
    '''
    Function for asking and reading user input from keyboard. 
    User is asked the question (text: string) until the input satisfies
    the requirements for the answer (options: [] & caseSens: bool).
    If user input is not valid, error message is shown (and question asked again).
    Returns
    -------
    <string>
        Read user input as string.
    '''
    while True:
        print(text, end='')
        answer = input()
        if (answer == '' and '' not in options):
            continue
        if (len(options) > 1):
            if (caseSens == True):
                if(answer not in options):
                    if (len(error) > 0):
                        print(error)
                    continue
            loweroptions = [x.lower() for x in options]
            if (answer.lower() not in loweroptions):
                if (len(error) > 0):
                    print(error)
                continue
        return answer

def get_user_input_int(text, low, high, error):
    '''
    Function for asking and reading user input from keyboard.
    Input must be integer number from low (param) to high (param).
    Returns
    -------
    <integer>
        Read user input as integer.
    '''
    while True:
        print(text, end='')
        try:
            num = int(input())
            if (num >= low and num <= high):
                return num
            else:
                continue
        except:
            continue
