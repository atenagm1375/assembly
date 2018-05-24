; exercise No.1, 08-Assembly3.pdf
; write a program that computes the LCM of 2 numbers{(RAX, RBX)->RDX}.
; run commands:
; nasm -f elf64 lcm.asm
; ld -o ./lcm -e _start ./lcm.o
; gdb ./lcm
; b exit
; r
; i r rdx
; c
; q
section .data
    a dq 54
    b dq 90

section .text
    global _start

_start:
    mov rax, [a]
    mov rbx, [b]
    call LCM

exit:
    mov rax, 1
    mov rbx, 0
    int 80h

LCM:
    mov r8, rax
    mov r9, rbx
    cmp rax, rbx
    jge while
    xchg rax, rbx
    while:
        xor rdx, rdx
        div rbx
        cmp rdx, 0
        jne continue
        mov rdx, rbx
        jmp end
        continue:
        mov rax, rbx
        mov rbx, rdx
        jmp while
    end:
    mov rax, r8
    mov rbx, r9
    mov rcx, rdx
    mul rbx
    xor rdx, rdx
    div rcx
    mov rdx, rax
    ret
