#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define CIRCLE_INVALID -1
#define CIRCLE_EMPTY 0
#define CIRCLE_YELLOW 1
#define CIRCLE_RED 2
#define CIRCLE_DRAW 3

typedef struct board
{
	char holes[6 * 7];
} board;

int c4Get(board *b, int col, int level)
{
	if (col < 0 || col > 6 || level < 0 || level > 5)
		return CIRCLE_INVALID;
	return b->holes[(5 * 7) + col - (level * 7)];
}

void c4Set(board *b, int col, int level, int value)
{
	if (col < 0 || col > 6 || level < 0 || level > 5)
		return;
	b->holes[(5 * 7) + col - (level * 7)] = value;
}

void c4Clean(board *b)
{
	memset(b->holes, CIRCLE_EMPTY, sizeof(b->holes));
}

void c4Copy(board *dst, board *src)
{
	memcpy(dst->holes, src->holes, sizeof(dst->holes));
}

int c4ColIsFull(board *b, int col)
{
	return c4Get(b, col, 5) != CIRCLE_EMPTY;
}

int c4Drop(board *b, int col, int value)
{
	if (c4ColIsFull(b, col))
		return 0;
	for (int level = 0; level < 6; level++)
	{
		if (c4Get(b, col, level) == CIRCLE_EMPTY)
		{
			c4Set(b, col, level, value);
			break;
		}
	}
	return 1;
}

void c4Print(board *b)
{
	for (int level = 5; level >= 0; level--)
	{
		for (int col = 0; col < 7; col++)
		{
			int color = c4Get(b, col, level);
			char *set = " YR";
			printf("[%c]", set[color]);
		}
		printf("\n");
	}
	for (int col = 0; col < 7; col++)
		printf(" %d ", col);
	printf("\n");
}

int c4GetWinner(board *b)
{
	int empty = 0;
	for (int level = 5; level >= 0; level--)
	{
		for (int col = 0; col < 7; col++)
		{
			int color = c4Get(b, col, level);
			if (color == CIRCLE_EMPTY)
			{
				empty++;
				continue;
			}

			struct
			{
				int col_incr;
				int level_incr;
			} dir[4] = {
				{1, 0},
				{0, 1},
				{1, 1},
				{-1, 1}};

			for (int d = 0; d < 4; d++)
			{

				int start_col = col;
				int start_level = level;
				while (c4Get(b, start_col - dir[d].col_incr,
							 start_level - dir[d].level_incr) == color)
				{
					start_col -= dir[d].col_incr;
					start_level -= dir[d].level_incr;
				}

				int count = 0;
				while (c4Get(b, start_col, start_level) == color)
				{
					count++;
					start_col += dir[d].col_incr;
					start_level += dir[d].level_incr;
				}
				if (count >= 4)
					return color;
			}
		}
	}
	return empty ? CIRCLE_EMPTY : CIRCLE_DRAW;
}

int c4RandomGame(board *b, int tomove)
{
	while (1)
	{
		if (c4Drop(b, rand() % 7, tomove))
		{
			tomove = (tomove == CIRCLE_YELLOW) ? CIRCLE_RED : CIRCLE_YELLOW;
		}
		int winner = c4GetWinner(b);
		if (winner != CIRCLE_EMPTY)
			return winner;
	}
}

int c4SuggestMove(board *b, int tomove)
{
	int best = -1;
	double best_ratio = 0;
	int games_per_move = 10000;
	for (int move = 0; move < 7; move++)
	{
		if (c4ColIsFull(b, move))
			continue;
		int won = 0, lost = 0;
		for (int j = 0; j < games_per_move; j++)
		{
			board copy;
			c4Copy(&copy, b);
			c4Drop(&copy, move, tomove);
			if (c4GetWinner(&copy) == tomove)
				return move;
			int next = (tomove == CIRCLE_YELLOW) ? CIRCLE_RED : CIRCLE_YELLOW;
			int winner = c4RandomGame(&copy, next);
			if (winner == CIRCLE_YELLOW || winner == CIRCLE_RED)
			{
				if (winner == tomove)
				{
					won++;
				}
				else
				{
					lost++;
				}
			}
		}
		double ratio = (double)won / (lost + 1);
		printf("Move %d ratio: %f\n", move, ratio);
		if (ratio > best_ratio || best == -1)
		{
			best = move;
			best_ratio = ratio;
		}
	}
	return best;
}

void c4Play(void)
{
	board b;
	c4Clean(&b);

	while (1)
	{
		c4Print(&b);
		if (c4GetWinner(&b) != CIRCLE_EMPTY)
			break;

		int human_move = -1;
		while (human_move == -1)
		{
			printf("Red, state your move: ");
			fflush(stdout);
			char buf[32];
			fgets(buf, sizeof(buf), stdin);
			human_move = atoi(buf);

			if (human_move > 6)
				human_move = -1;
			if (human_move < 0)
				human_move = -1;
			if (human_move != -1 && c4ColIsFull(&b, human_move))
				human_move = -1;
		}
		c4Drop(&b, human_move, CIRCLE_RED);

		int computer_move = c4SuggestMove(&b, CIRCLE_YELLOW);
		c4Drop(&b, computer_move, CIRCLE_YELLOW);
	}
}

int main(void)
{
	srand(time(NULL));
	c4Play();
}
