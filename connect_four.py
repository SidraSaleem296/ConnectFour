import random

# Constants
ROWS = 6
COLS = 7
EMPTY = 0
PLAYER_1 = 1
PLAYER_2 = 2

class ConnectFour:
    def __init__(self):
        self.board = [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]
        self.current_player = PLAYER_1
    
    def print_board(self):
        """Print the current game board."""
        for row in self.board:
            print(" | ".join(str(cell) if cell != EMPTY else "." for cell in row))
            print("-" * (COLS * 4 - 1))

    def drop_piece(self, col):
        """Drop a piece in the given column."""
        if col < 0 or col >= COLS:
            raise ValueError("Invalid column. Must be between 0 and 6.")
        
        # Find the first available row in the column
        for row in range(ROWS-1, -1, -1):
            if self.board[row][col] == EMPTY:
                self.board[row][col] = self.current_player
                return row, col
        raise ValueError(f"Column {col} is full.")
    
    def check_win(self, row, col):
        """Check if the current player has won after dropping a piece."""
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dr, dc in directions:
            count = 1
            for i in range(1, 4):
                r, c = row + dr * i, col + dc * i
                if 0 <= r < ROWS and 0 <= c < COLS and self.board[r][c] == self.current_player:
                    count += 1
                else:
                    break
            for i in range(1, 4):
                r, c = row - dr * i, col - dc * i
                if 0 <= r < ROWS and 0 <= c < COLS and self.board[r][c] == self.current_player:
                    count += 1
                else:
                    break
            if count >= 4:
                return True
        return False
    
    def switch_player(self):
        """Switch turns between player 1 and player 2."""
        self.current_player = PLAYER_2 if self.current_player == PLAYER_1 else PLAYER_1
    
    def is_full(self):
        """Check if the board is full."""
        return all(self.board[0][col] != EMPTY for col in range(COLS))
    
    def play_game(self, ai_strategy=None):
        """Simulate a full game with alternating players."""
        while not self.is_full():
            valid_move = False
            while not valid_move:
                if self.current_player == PLAYER_1:
                    # Player 1 (AI) uses the AI strategy
                    col = ai_strategy()
                else:
                    # Player 2 (human) uses random moves or another AI
                    col = random.randint(0, 6)
                try:
                    row, col = self.drop_piece(col)
                    if self.check_win(row, col):
                        self.print_board()
                        print(f"Player {self.current_player} wins!")
                        return
                    valid_move = True
                    self.switch_player()
                except ValueError:
                    continue
        self.print_board()
        print("It's a draw!")


class GeneticAI:
    def __init__(self, population_size=50, mutation_rate=0.05, generations=100):
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.generations = generations
        self.population = self.generate_population()
    
    def generate_population(self):
        """Generate an initial population of strategies."""
        return [[random.randint(0, COLS-1) for _ in range(ROWS)] for _ in range(self.population_size)]
    
    def fitness(self, strategy):
        """Evaluate the fitness of a strategy by simulating games."""
        game = ConnectFour()
        fitness_score = 0
        for move in strategy:
            try:
                row, col = game.drop_piece(move)  # Drop the piece and get the row, column where it landed
                if game.check_win(row, col):  # Pass both row and col to check for a win
                    fitness_score += 1  # AI wins
            except ValueError:
                continue  # Invalid move, try next strategy
        return fitness_score
    
    def selection(self):
        """Select two strategies based on fitness."""
        selected = random.choices(self.population, k=2, weights=[self.fitness(ind) for ind in self.population])
        return selected[0], selected[1]
    
    def crossover(self, parent1, parent2):
        """Crossover between two parents to create a new strategy."""
        crossover_point = random.randint(1, len(parent1)-1)
        child = parent1[:crossover_point] + parent2[crossover_point:]
        return child
    
    def mutation(self, strategy):
        """Randomly mutate a strategy."""
        if random.random() < self.mutation_rate:
            mutation_index = random.randint(0, len(strategy)-1)
            strategy[mutation_index] = random.randint(0, COLS-1)
        return strategy
    
    def evolve(self):
        """Run the genetic algorithm for multiple generations."""
        for generation in range(self.generations):
            new_population = []
            for _ in range(self.population_size // 2):
                parent1, parent2 = self.selection()
                child1 = self.crossover(parent1, parent2)
                child2 = self.crossover(parent2, parent1)
                new_population.append(self.mutation(child1))
                new_population.append(self.mutation(child2))
            self.population = new_population
            print(f"Generation {generation + 1}: Best fitness: {max([self.fitness(ind) for ind in self.population])}")


# Example Usage of GeneticAI
ai_player = GeneticAI()

# Evolve the population for a number of generations
ai_player.evolve()

# Example strategy that selects the best move based on AI
def ai_strategy():
    """AI selects a column based on its best evolved strategy."""
    return random.choice(ai_player.population[0])  # Select from the best individual

# Start a game with the evolved AI playing against a random player
game = ConnectFour()
game.play_game(ai_strategy)
