; exercise page 26, 10-assembly4.pdf
; write a program to do bitwise-reverse for 64-bit data{rax->rdx}.
section .text
    global _start

_start:
    mov rax, 0x00e8
    call reverse

exit:
    mov rax, 1
    mov rbx, 0
    int 80h

reverse:
    xor rdx, rdx
    do:
        mov rbx, 63
        bsf rcx, rax
        jz end
        sub rbx, rcx
        bts rdx, rbx
        btc rax, rcx
        jmp do
    end:
    ret
