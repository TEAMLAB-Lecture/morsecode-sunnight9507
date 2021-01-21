# -*- coding: utf8 -*-
import re


# Help Function - 수정하지 말 것
def get_morse_code_dict():
    morse_code = {
        "A": ".-",
        "N": "-.",
        "B": "-...",
        "O": "---",
        "C": "-.-.",
        "P": ".--.",
        "D": "-..",
        "Q": "--.-",
        "E": ".",
        "R": ".-.",
        "F": "..-.",
        "S": "...",
        "G": "--.",
        "T": "-",
        "H": "....",
        "U": "..-",
        "I": "..",
        "V": "...-",
        "K": "-.-",
        "X": "-..-",
        "J": ".---",
        "W": ".--",
        "L": ".-..",
        "Y": "-.--",
        "M": "--",
        "Z": "--..",
    }
    return morse_code


# Help Function - 수정하지 말 것
def get_help_message():
    message = "HELP - International Morse Code List\n"
    morse_code = get_morse_code_dict()

    counter = 0

    for key in sorted(morse_code):
        counter += 1
        message += "%s: %s\t" % (key, morse_code[key])
        if counter % 5 == 0:
            message += "\n"

    return message


def is_help_command(user_input):
    """
    Input:
        - user_input : 문자열값으로 사용자가 입력하는 문자
    Output:
        - 입력한 값이 대소문자 구분없이 "H" 또는 "HELP"일 경우 True,
          그렇지 않을 경우 False를 반환함
    Examples:
        >>> import morsecode as mc
        >>> mc.is_help_command("H")
        True
        >>> mc.is_help_command("Help")
        True
        >>> mc.is_help_command("Half")
        False
        >>> mc.is_help_command("HeLp")
        True
        >>> mc.is_help_command("HELLO")
        False
        >>> mc.is_help_command("E")
        False
    """
    upper_user_input = user_input.upper()
    result = upper_user_input == "H" or upper_user_input == "HELP"
    return result


def is_validated_english_sentence(user_input):
    """
    Input:
        - user_input : 문자열값으로 사용자가 입력하는 문자
    Output:
        - 입력한 값이 아래에 해당될 경우 False, 그렇지 않으면 True
          1) 숫자가 포함되어 있거나,
          2) _@#$%^&*()-+=[]{}"';:\|`~ 와 같은 특수문자가 포함되어 있거나
          3) 문장부호(.,!?)를 제외하면 입력값이 없거나 빈칸만 입력했을 경우
    Examples:
        >>> import morsecode as mc
        >>> mc.is_validated_english_sentence("Hello 123")
        False
        >>> mc.is_validated_english_sentence("Hi!")
        True
        >>> mc.is_validated_english_sentence(".!.")
        False
        >>> mc.is_validated_english_sentence("!.!")
        False
        >>> mc.is_validated_english_sentence("kkkkk... ^^;")
        False
        >>> mc.is_validated_english_sentence("This is Gachon University.")
        True
    """
    # 1) 숫자 포함 여부
    is_string_in_number = any(i.isdecimal() for i in user_input)
    if is_string_in_number:
        return False
    # 2) 특수 문자 포함 여부
    special_symbols = set("_@#$%^&*()-+=[]{}\"';:\|`~")
    is_string_in_special_symbols = any(i in special_symbols for i in user_input)
    if is_string_in_special_symbols:
        return False
    # 3) 문장 부호 제거 후 값 존재 여부
    punctuation_marks = "[.,!?]"
    result_string = re.sub(punctuation_marks, "", user_input)
    result_string = result_string.strip()
    # 값이 존재하지 않을 경우
    if not result_string:
        return False
    return True


def is_validated_morse_code(user_input):
    """
    Input:
        - user_input : 문자열값으로 사용자가 입력하는 문자
    Output:
        - 입력한 값이 아래에 해당될 경우 False, 그렇지 않으면 True
          1) "-","."," "외 다른 글자가 포함되어 있는 경우
          2) get_morse_code_dict 함수에 정의된 Morse Code 부호외 다른 코드가 입력된 경우 ex)......
    Examples:
        >>> import morsecode as mc
        >>> mc.is_validated_morse_code("..")
        True
        >>> mc.is_validated_morse_code("..-")
        True
        >>> mc.is_validated_morse_code("..-..")
        False
        >>> mc.is_validated_morse_code(". . . .")
        True
        >>> mc.is_validated_morse_code("-- -- -- --")
        True
        >>> mc.is_validated_morse_code("!.1 abc --")
        False
    """
    # 1) "-","."," "외 글자 확인
    possible_string = {"-", ".", " "}
    is_not_possible_string = any(i not in possible_string for i in user_input)
    if is_not_possible_string:
        return False
    # 2) get_morse_code_dict외 다른 부호 존재 여부
    morse_code_dict = get_morse_code_dict()
    morse_codes = {code for code in morse_code_dict.values()}  # morse code 부호 추출
    user_input_list = user_input.split()
    is_not_morse_code = any(i not in morse_codes for i in user_input_list)
    if is_not_morse_code:
        return False
    return True


def get_cleaned_english_sentence(raw_english_sentence):
    """
    Input:
        - raw_english_sentence : 문자열값으로 Morse Code로 변환 가능한 영어 문장
    Output:
        - 입력된 영어문장에수 4개의 문장부호를 ".,!?" 삭제하고, 양쪽끝 여백을 제거한 문자열 값 반환
    Examples:
        >>> import morsecode as mc
        >>> mc.get_cleaned_english_sentence("This is Gachon!!")
        'This is Gachon'
        >>> mc.get_cleaned_english_sentence("Is this Gachon?")
        'Is this Gachon'
        >>> mc.get_cleaned_english_sentence("How are you?")
        'How are you'
        >>> mc.get_cleaned_english_sentence("Fine, Thank you. and you?")
        'Fine Thank you and you'
    """
    # 1) 양쪽끝 여백 제거 2)에서 불필요한 iteration이 있을 수 있으므로 미리 제거
    raw_english_sentence = raw_english_sentence.strip()
    # 2) 조건의 4개의 문장부호 삭제
    punctuation_marks = "[.,!?]"
    cleaned_string = re.sub(punctuation_marks, "", raw_english_sentence)
    return cleaned_string


def decoding_character(morse_character):
    """
    Input:
        - morse_character : 문자열값으로 get_morse_code_dict 함수로 알파벳으로 치환이 가능한 값의 입력이 보장됨
    Output:
        - Morse Code를 알파벳으로 치환한 값
    Examples:
        >>> import morsecode as mc
        >>> mc.decoding_character("-")
        'T'
        >>> mc.decoding_character(".")
        'E'
        >>> mc.decoding_character(".-")
        'A'
        >>> mc.decoding_character("...")
        'S'
        >>> mc.decoding_character("....")
        'H'
        >>> mc.decoding_character("-.-")
        'K'
    """
    # 해당 함수는 매칭되는 값만 전해주기 때문에 key value를 바꾼 새로운 dictionary를 생성해 메모리를 차지할 필요가 없다.
    # 단순히 morse_code_dict iter
    morse_code_dict = get_morse_code_dict()
    for string, morce_code in morse_code_dict.items():
        if morse_character == morce_code:
            return string


def encoding_character(english_character):
    """
    Input:
        - english_character : 문자열값으로 알파벳 한 글자의 입력이 보장됨
    Output:
        - get_morse_code_dict 함수의 반환 값으로 인해 변환된 모스부호 문자열값
    Examples:
        >>> import morsecode as mc
        >>> mc.encoding_character("G")
        '--.'
        >>> mc.encoding_character("A")
        '.-'
        >>> mc.encoding_character("C")
        '-.-.'
        >>> mc.encoding_character("H")
        '....'
        >>> mc.encoding_character("O")
        '---'
        >>> mc.encoding_character("N")
        '-.'
    """
    morse_code_dict = get_morse_code_dict()
    return morse_code_dict[english_character]


def decoding_sentence(morse_sentence):
    """
    Input:
        - morse_sentence : 문자열 값으로 모스 부호를 표현하는 문자열
    Output:
        - 모스부호를 알파벳으로 변환한 문자열
    Examples:
        >>> import morsecode as mc
        >>> mc.decoding_sentence("... --- ...")
        'SOS'
        >>> mc.decoding_sentence("--. .- -.-. .... --- -.")
        'GACHON'
        >>> mc.decoding_sentence("..  .-.. --- ...- .  -.-- --- ..-")
        'I LOVE YOU'
        >>> mc.decoding_sentence("-.-- --- ..-  .- .-. .  ..-. ")
        'YOU ARE F'
    """
    morse_code_list = morse_sentence.split(" ")
    result = ""
    return "".join(map(lambda x: decoding_character(x) if x else " ", morse_code_list))


def encoding_sentence(english_sentence):
    """
    Input:
        - english_sentence : 문자열 값으로 모스 부호로 변환이 가능한 영어문장
    Output:
        - 입력된 영어문장 문자열 값을 모스부호로 변환된 알파벳으로 변환한 문자열
          단 양쪽 끝에 빈칸은 삭제한다.
    Examples:
        >>> import morsecode as mc
        >>> mc.encoding_sentence("HI! Fine, Thank you.")
        '.... ..  ..-. .. -. .  - .... .- -. -.-  -.-- --- ..-'
        >>> mc.encoding_sentence("Hello! This is CS fifty Class.")
        '.... . .-.. .-.. ---  - .... .. ...  .. ...  -.-. ...  ..-. .. ..-. - -.--  -.-. .-.. .- ... ...'
        >>> mc.encoding_sentence("We Are Gachon")
        '.-- .  .- .-. .  --. .- -.-. .... --- -.'
        >>> mc.encoding_sentence("Hi! Hi!")
        '.... ..  .... ..'
    """
    cleaned_english_sentence = get_cleaned_english_sentence(english_sentence).upper()
    words = cleaned_english_sentence.split()
    morse_code_dict = get_morse_code_dict()  # function encoding_character의 필요성에 대한 의문
    result = ""
    for word in words:
        for string in word:
            if string in morse_code_dict:
                result += " " + morse_code_dict[string]
        result += " "
    return result.strip()


def main():
    print("Morse Code Program!!")
    is_not_zero = True
    while is_not_zero:
        user_input = input("Input your message(H - Help, 0 - Exit): ")
        # 1) 0 입력시 종료
        if user_input == "0":
            is_not_zero = False
        # 2) help 호출
        elif is_help_command(user_input):
            print(get_help_message())
        # 3) 모스부호로 변환이 가능한 알파벳 문장
        elif is_validated_english_sentence(user_input):
            print(encoding_sentence(user_input))
        # 4) 알파벳으로 변환이 가능한 모스부호
        elif is_validated_morse_code(user_input):
            print(decoding_sentence(user_input))
        # 5) 그 외 변환이 불가능한 입력
        else:
            print("Wrong Input")
    print("Good Bye")
    print("Morse Code Program Finished!!")


if __name__ == "__main__":
    main()
