#include "bits/stdc++.h"
using namespace std;

const int N = 24, L = 70; 
char squares[L][L];

bool fits(int row, int col, int size) {
    // czy kwadrat o boku size się zmieści
    if (row + size > L || col + size > L) return false;

    // sprawdzamy czy pola są wolne
    for (int i = 0; i < size; i++)
        for (int j = 0; j < size; j++)
            if (squares[i + row][j + col]) return false;

    return true;
}

void fill(int row, int col, int size) {
    // wypełniamy
    for (int i = 0; i < size; i++) {
        for (int j = 0; j < size; j++) {
            squares[i + row][j + col] = 'A' + size - 1;
        }
    }
}

int main() {
    for (int size = N; size > 0; size--) {
        bool found = true;
        for (int row = 0; row < L && found; row++) {
            for (int col = 0; col < L && found; col++) {
                if (fits(row, col, size)) {
                    fill(row, col, size);
                    found = false;
                    break;
                }
            }
        }
    }

    int empty = 0;
    for(auto &i : squares) {
        for(auto j : i){
            if(!j) {
                empty++;
                cout << '.';
            } else cout << j;
        }
        cout << '\n';
    }
    cout << empty << '\n';
}