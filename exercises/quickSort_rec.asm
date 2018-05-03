; exercise No.1, 11-assembly5.pdf
; implement quick sort algorithm using recursive approach.
; run commands:
; nasm -f elf32 quickSort_rec.asm
; ld -m elf_i386 quickSort_rec.o -o quickSort_rec
; gdb ./quickSort_rec
; b exit
; r
; i r eax //this is the index of array were the key is found(-1 if not found)
; c
; q
%define low [ebp+12]
%define high [ebp+8]
section .data
    src dd 12, 50, 1, 6, 5, 4, 7, 9, 10, 8, 6, 3, 22, 0, 29, 2
    len equ ($-src)/4

section .bss
    arr resd len

section .text
    global _start

_start:
    mov esi, src
    mov edi, arr
    mov ecx, len
    transfer_while:
        mov eax, [esi]
        mov [edi], eax
        add esi, 4
        add edi, 4
        loop transfer_while
    mov esi, arr
    push 0
    mov ecx, len
    dec ecx
    push ecx
    call quickSort
    mov ecx, len
    check:
        mov eax, [esi]
        add esi, 4
        loop check

exit:
    mov eax, 1
    mov ebx, 0
    int 80h

quickSort:
    enter 4, 0
    mov ecx, high
    cmp low, ecx
    jge finish
    push dword low
    push dword high
    call partition
    mov [ebp-4], eax
    xor eax, eax
    push dword low
    mov ecx, [ebp-4]
    dec ecx
    push ecx
    call quickSort
    mov ecx, [ebp-4]
    inc ecx
    push ecx
    push dword high
    call quickSort
    finish:
    leave
    ret 8

partition:
    enter 12, 0
    %define pivot [ebp-12]
    %define i [ebp-8]
    %define j [ebp-4]
    mov ecx, high
    mov ebx, [esi+ecx*4]
    mov pivot, ebx
    mov ebx, low
    mov i, ebx
    dec dword i
    mov j, ebx
    while:
        mov ecx, high
        cmp j, ecx
        jge end_while
        mov ebx, j
        mov edx, [esi+ebx*4]        ; edx = arr[j]
        cmp edx, pivot
        jg end_if
        inc dword i
        mov ebx, i
        xchg edx, [esi+ebx*4]
        mov ebx, j
        mov [esi+ebx*4], edx
        end_if:
        inc dword j
        jmp while
    end_while:
    mov eax, i
    inc eax
    mov edx, [esi+eax*4]
    mov ecx, high
    xchg edx, [esi+ecx*4]
    mov [esi+eax*4], edx
    leave
    ret 8
