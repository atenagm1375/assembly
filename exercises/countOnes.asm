; exercise No.1, 10-assembly4.pdf
; write a program that counts those bits of rax that are 1.
; run commands:
; nasm -f elf64 countOnes.asm
; ld -o ./countOnes -e _start ./countOnes.o
; gdb ./countOnes
; b exit
; r
; i r cx
; c
; q
section .text
    global _start

_start:
    mov rax, 0xf302e1
    call countOnes

exit:
    mov rax, 1
    mov rbx, 0
    int 80h

countOnes:
    xor cx, cx
    while:
        bsf rbx, rax
        jz end
        inc cx
        btc rax, rbx
        jmp while
    end:
    ret
