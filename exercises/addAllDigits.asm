; exercise No.6, 08-Assembly.pdf
; write a program that computes some of all digits of a number{AX->DX}.
; run commands:
; nasm -f elf64 addAllDigits.asm
; ld -o ./addAllDigits -e _start ./addAllDigits.o
; gdb ./addAllDigits
; b exit
; r
; i r dx
; c
; q
section .text
    global _start

_start:
    mov ax, 1496
    call addAllDigits

exit:
    mov rax, 1
    mov rbx, 0
    int 80h

addAllDigits:
    mov r10w, 10
    xor cx, cx
    while:
        xor dx, dx
        div r10w
        add cx, dx
        cmp ax, 0
        jne while
    mov dx, cx
    ret
