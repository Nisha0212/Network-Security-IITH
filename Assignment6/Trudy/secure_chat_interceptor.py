from downgrade_attack import down_grade_attack
from MITM_attack import M_I_T_M
from sys import argv

def main():
    if (len(argv) == 4):
        if(argv[1] == "-d"):
            down_grade_attack(argv[2], argv[3])
        elif(argv[1] == "-m"):
            M_I_T_M(argv[2], argv[3])
    else:
        print("Usage -> \n down grade attack: -d <client> <server>\n MITM attack: -m <client> <server>")
        exit()

main()

