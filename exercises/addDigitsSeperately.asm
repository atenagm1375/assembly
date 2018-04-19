; exercise No.7, 08-Assembly3.pdf
; write a program that computes sum of even and odd digits seperately{AX->(BX, DX)}.
; run commands:
; nasm -f elf64 addDigitsSeperately.asm
; ld -o ./addDigitsSeperately -e _start ./addDigitsSeperately.o
; gdb ./addDigitsSeperately
; b exit
; r
; i r bx
; i r dx
; c
; q
section .text
    global _start

_start:
    mov ax, 1469
    call addDigitsSeperately

exit:
    mov rax, 1
    mov rbx, 0
    int 80h

addDigitsSeperately:
    xor cx, cx
    while:
        mov r10w, 10
        xor dx, dx
        div r10w
        mov r11w, dx
        mov r12w, ax
        xor dx, dx
        mov ax, cx
        mov r10w, 2
        div r10w
        cmp dx, 0
        je even
        add r8w, r11w
        jmp afterEven
        even:
        add r9w, r11w
        afterEven:
        mov ax, r12w
        inc cx
        cmp ax, 0
        jne while
    xor dx, dx
    mov ax, cx
    div r10w
    cmp dx, 0
    je odd
    mov dx, r8w
    mov bx, r9w
    ret
    odd:
    mov dx, r9w
    mov bx, r8w
    ret
