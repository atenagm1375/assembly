; exercise on page 33, 08-Assembly3.pdf
; write a program that converts bcd number into binary{AX->AL}.
; run commands:
; nasm -f elf64 bcd2bin.asm
; ld -o ./bcd2bin -e _start ./bcd2bin.o
; gdb ./bcd2bin
; b exit
; r
; i r ax
; c
; q
section .text
    global _start

_start:
    mov al, 245
    call Bin2BCD                ; this is the code we reviewed in class which is reverse of what we do in the following
    call BCD2Bin

exit:
    mov rax, 1
    mov rbx, 0
    int 80h

Bin2BCD:
    mov bl, 10
    mov ah, 0
    div bl
    mov bh, ah
    xor ah, ah
    div bl
    shl ah, 4
    or bh, ah
    mov ah, al
    mov al, bh
    ret

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
