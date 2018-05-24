; exercise No.5, 08-Assembly3.pdf
; write a program that computes GCD of two numbers{(AX, BX)->DX}.
; run commands:
; nasm -f elf64 gcd.asm
; ld -o ./gcd -e _start ./gcd.o
; gdb ./gcd
; b exit
; r
; i r dx
; c
; q
section .data
    a dw 54
    b dw 90

section .text
    global _start

_start:
    mov ax, [a]
    mov bx, [b]
    call GCD

exit:
    mov rax, 1
    mov rbx, 0
    int 80h

GCD:
    cmp ax, bx
    jge while
    xchg ax, bx
    while:
        xor dx, dx
        div bx
        cmp dx, 0
        jne continue
        mov dx, bx
        jmp end
        continue:
        mov ax, bx
        mov bx, dx
        jmp while
    end:
    ret
