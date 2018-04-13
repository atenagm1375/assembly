; exercise No.2, 10-assembly4.pdf
; write a program that counts number of bits valued 1 between esi and edi.
section .data
    a db 32, 25, 4, 8, 3, 9, 6, 0, 0, 1, 5, 7
    len equ $-a

section .text
    global _start

_start:
    lea esi, [a]
    lea edi, [a+len]
    call countBits

exit:
    mov rax, 1
    mov rbx, 0
    int 80h

countBits:
    xor rcx, rcx
    while1:
        cmp esi, edi
        jge end_while1
        movzx ax, byte[esi]
        while2:
            bsf bx, ax
            jz end_while2
            inc rcx
            btc ax, bx
            jmp while2
        end_while2:
        inc esi
        jmp while1
    end_while1:
    ret
