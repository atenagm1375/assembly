; exercise No.1, 12-Assembly6.pdf
; write a program to compute mean of 100 floating point values.
; run commands:
; nasm -f elf64 computeMean.asm
; ld -o ./computeMean -e _start ./computeMean.o
; gdb ./computeMean
; b exit
; r
; i r st0
; c
; q
section .data
    src dq 1.e0,2.e0,3.e0,4.e0,5.e0,6.e0,7.e0,8.e0,9.e0,1.e1,\
            1.e0,2.e0,3.e0,4.e0,5.e0,6.e0,7.e0,8.e0,9.e0,1.e1,\
            1.e0,2.e0,3.e0,4.e0,5.e0,6.e0,7.e0,8.e0,9.e0,1.e1,\
            1.e0,2.e0,3.e0,4.e0,5.e0,6.e0,7.e0,8.e0,9.e0,1.e1,\
            1.e0,2.e0,3.e0,4.e0,5.e0,6.e0,7.e0,8.e0,9.e0,1.e1,\
            1.e0,2.e0,3.e0,4.e0,5.e0,6.e0,7.e0,8.e0,9.e0,1.e1,\
            1.e0,2.e0,3.e0,4.e0,5.e0,6.e0,7.e0,8.e0,9.e0,1.e1,\
            1.e0,2.e0,3.e0,4.e0,5.e0,6.e0,7.e0,8.e0,9.e0,1.e1,\
            1.e0,2.e0,3.e0,4.e0,5.e0,6.e0,7.e0,8.e0,9.e0,1.e1,\
            1.e0,2.e0,3.e0,4.e0,5.e0,6.e0,7.e0,8.e0,9.e0,1.e1
    len equ ($-src)/8
    a dq 0

section .bss
    arr resq len

section .text
    global _start

_start:
    mov rsi, src
    mov rdi, arr
    mov rcx, len
    transfer_while:
        mov rax, [rsi]
        mov [rdi], rax
        add rsi, 8
        add rdi, 8
        loop transfer_while
    call COMPUTEMEAN

exit:
    mov rax, 1
    mov rbx, 0
    int 80h

COMPUTEMEAN:
    mov rsi, arr
    mov rcx, len
    mov [a], rcx
    fild qword[a]
    fldz
    add_loop:
        dec rcx
        fadd qword[rsi+rcx*8]
        cmp rcx, 0
        jnz add_loop
    fdiv ST1
    fst qword[a]
    ret
