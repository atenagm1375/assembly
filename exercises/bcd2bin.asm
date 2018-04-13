; exercise on page 33, 08-Assembly3.pdf
; write a program that converts bcd number into binary{AX->AL}.
section .text
    global _start

_start:
    mov rax, 0x0245
    call BCD2Bin

exit:
    mov rax, 1
    mov rbx, 1
    int 80h

BCD2Bin:
    mov cl, ah
    mov bl, 16
    xor ah, ah
    div bl
    add dl, ah
    xor ah, ah
    mov bl, 10
    mul bl
    add dl, al
    mov al, cl
    mov bl, 100
    mul bl
    add al, dl
    ret
