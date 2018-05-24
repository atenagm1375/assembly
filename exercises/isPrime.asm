;exercise No.3, 08-Assembly3.pdf
; write a program that says whether the number in rax is prime ro not.
; run commands:
; nasm -f elf64 isPrime.asm
; ld -o ./isPrime -e _start ./isPrime.o
; gdb ./isPrime
; b exit
; r
; i r r9
; c
; q
section .text
    global _start

_start:
    mov rax, 37
    call isPrime

exit:
    mov rax, 1
    mov rbx, 0
    int 80h

isPrime:
    cmp rax, 1
    jle end
    mov rbx, 1
    cmp rax, 2
    cmovz r9, rbx
    jz end
    mov r8, rax
    mov rbx, 2
    div rbx
    cmp dx, 0
    je end
    inc rbx
    while:
        cmp rbx, r8
        jge end_while
        xor rdx, rdx
        mov rax, r8
        div rbx
        cmp rdx, 0
        je end
        add rbx, 2
        jmp while
    end_while:
    mov r9, 1
    end:
    ret
