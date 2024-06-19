#include "bits/stdc++.h"

const int N = 24, L = 70; 
char squares[L][L];

bool fits(int row, int col, int size) 
{
    // Will square of size side fit
    if (row + size > L or col + size > L) return false;

    // check if fields are free
    for (int i = 0; i < size; ++i)
        for (int j = 0; j < size; ++j)
            if (squares[i + row][j + col]) return false;

    return true;
}

void fill(int row, int col, int size)
{
    for (int i = 0; i < size; ++i) 
        for (int j = 0; j < size; ++j) 
            squares[i + row][j + col] = 'A' + size - 1;
}

void print_board()
{
    int empty_fields_counter = 0;

    for (const auto& squares_in_row : squares) {
        for (auto square : squares_in_row){
            if (not square)
            {
                empty_fields_counter++;
                std::cout << ". ";
            } 
            else std::cout << square << " ";
        }
        std::cout << '\n';
    }
    std::cout << empty_fields_counter << '\n';
}

int main() {
    for (int size = N; size > 0; --size) {
        bool found = true;
        for (int row = 0; row < L and found; ++row) {
            for (int col = 0; col < L and found; ++col) {
                if (fits(row, col, size)) 
                {
                    fill(row, col, size);
                    found = false;
                    break;
                }
            }
        }
    }
    print_board();
}