; exercise No.2, 11-assembly5.pdf
; implement binary search algorithm using recursive approach.
; run commands:
; nasm -f elf32 binarySearch_rec.asm
; ld -m elf_i386 binarySearch_rec.o -o binarySearch_rec
; gdb ./binarySearch_rec
; b exit
; r
; i r eax //this is the index of array were the key is found(-1 if not found)
; c
; q
section .data
    array dd 1, 4, 6, 7, 12, 16, 21, 34, 49, 50, 53, 54, 55, 60, 99, 100
    len equ ($-array)/4
    key dd 50
    index db -1

section .text
    global _start

_start:
    xor eax, eax
    push eax
    mov eax, len
    dec eax
    push eax
    call binarySearch
    movsx eax, byte[index]

exit:
    mov eax, 1
    mov ebx, 0
    int 80h

binarySearch:
    enter 4, 0
    mov ebx, dword[ebp+12]
    mov ecx, dword[ebp+8]
    cmp ebx, ecx
    jle rec
    leave
    ret 8

    rec:
    xor eax, eax
    xor edx, edx
    mov esi, 2
    mov eax, ebx
    add eax, ecx
    div esi
    xor edx, edx
    mov [ebp-4], eax
    mov esi, 4
    mul esi
    mov edi, array
    add edi, eax
    mov eax, dword[key]
    mov edx, [edi]
    cmp eax, edx
    jl search_left
    jg search_right
    mov eax, dword[ebp-4]
    mov [index], eax
    xor ebx, ebx
    xor edx, edx
    leave
    ret 8

    search_left:
    push ebx
    dec dword[ebp-4]
    push dword[ebp-4]
    call binarySearch
    leave
    ret 8

    search_right:
    inc dword[ebp-4]
    push dword[ebp-4]
    push ecx
    call binarySearch
    leave
    ret 8
