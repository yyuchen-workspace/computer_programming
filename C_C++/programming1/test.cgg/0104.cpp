#include <stdio.h>
#include <stdlib.h>

#define NUM_CARDS 13

// Function to calculate HCP
int calculateHCP(int cards[]) {
    int hcp = 0;
    for (int i = 0; i < NUM_CARDS; i++) {
        int card = cards[i];
        if (card == 1 || card == 14 || card == 27 || card == 40) hcp += 4; // Ace
        else if (card == 11 || card == 24 || card == 37 || card == 50) hcp += 3; // King
        else if (card == 12 || card == 25 || card == 38 || card == 51) hcp += 2; // Queen
        else if (card == 13 || card == 26 || card == 39 || card == 52) hcp += 1; // Jack
    }
    return hcp;
}

// Function to count cards in each suit
void countSuits(int cards[], int suitCount[]) {
    for (int i = 0; i < NUM_CARDS; i++) {
        int card = cards[i];
        if (card >= 1 && card <= 13) suitCount[0]++; // ♠
        else if (card >= 14 && card <= 26) suitCount[1]++; // ♡
        else if (card >= 27 && card <= 39) suitCount[2]++; // ♢
        else if (card >= 40 && card <= 52) suitCount[3]++; // ♣
    }
}

int main() {
    int cards[NUM_CARDS];
    int suitCount[4] = {0}; // ♠, ♡, ♢, ♣
    int hcp;
    int balanced;

    // Read card inputs
    for (int i = 0; i < NUM_CARDS; i++) {
        if (scanf("%d", &cards[i]) != 1 || cards[i] < 1 || cards[i] > 52) {
            printf("Error: Invalid input.\n");
            return 1;
        }
    }

    // Calculate HCP
    hcp = calculateHCP(cards);

    // Count suits
    countSuits(cards, suitCount);

    // Check for balanced hand
    balanced = (suitCount[0] == 4 && suitCount[1] == 3 && suitCount[2] == 3 && suitCount[3] == 3) || 
               (suitCount[0] == 4 && suitCount[1] == 3 && suitCount[2] == 4 && suitCount[3] == 2) ||
               (suitCount[0] == 4 && suitCount[1] == 4 && suitCount[2] == 3 && suitCount[3] == 2) ||
               (suitCount[0] == 5 && suitCount[1] == 3 && suitCount[2] == 3 && suitCount[3] == 2) ||
               (suitCount[0] == 4 && suitCount[1] == 3 && suitCount[2] == 4 && suitCount[3] == 2);

    // Print HCP and suit distribution
    printf("HCP: %d pts\n", hcp);
    printf("Suit: %d-%d-%d-%d\n", suitCount[0], suitCount[1], suitCount[2], suitCount[3]);

    // Determine and print bidding choice
    if (hcp >= 16) {
        printf("The bidding choice: 1C\n");
    } else if (hcp >= 11 && hcp <= 15) {
        if (suitCount[2] >= 4) {
            printf("The bidding choice: 1D\n");
        } else if (suitCount[0] >= 5) {
            printf("The bidding choice: 1S\n");
        } else if (suitCount[1] >= 5) {
            printf("The bidding choice: 1H\n");
        } else if (suitCount[3] >= 6) {
            printf("The bidding choice: 2C\n");
        } else if (suitCount[3] >= 5 && suitCount[2] == 0) {
            printf("The bidding choice: 2D\n");
        } else if (suitCount[1] >= 6) {
            printf("The bidding choice: 2H\n");
        } else if (suitCount[0] >= 6) {
            printf("The bidding choice: 2S\n");
        } else if (balanced && hcp >= 13 && hcp <= 15) {
            printf("The bidding choice: 1NT\n");
        } else {
            printf("The bidding choice: Pass\n");
        }
    } else if (hcp >= 22 && hcp <= 24 && balanced) {
        printf("The bidding choice: 2NT\n");
    } else if (hcp >= 8 && hcp <= 11) {
        if (suitCount[0] >= 7) {
            printf("The bidding choice: 3S\n");
        } else if (suitCount[1] >= 7) {
            printf("The bidding choice: 3H\n");
        } else if (suitCount[2] >= 7) {
            printf("The bidding choice: 3D\n");
        } else if (suitCount[3] >= 7) {
            printf("The bidding choice: 3C\n");
        } else {
            printf("The bidding choice: Pass\n");
        }
    } else if (hcp < 16 && (suitCount[0] >= 7 || suitCount[1] >= 7)) {
        printf("The bidding choice: 3NT\n");
    } else {
        printf("The bidding choice: Pass\n");
    }

    return 0;
}