import csv, sys, math

class DecideByBracket:

    def __init__(self, competitors_csv_path, max_competitors=None):

        csv_file = open(competitors_csv_path)
        reader = csv.reader(csv_file)
        if max_competitors is None:
            self.competitors = list(reader)[1:]
        else:
            self.competitors = list(reader)[1:max_competitors+1]
        self.bracket = {}

        tmp = open('tournament_results.csv', 'w+')
        tmp.close()

        fieldnames = ['round', 'match_number', 'c1', 'c2', 'winner']
        self.out_file = open('tournament_results.csv', 'a+', newline='')
        self.writer = csv.DictWriter(self.out_file, fieldnames=fieldnames)
        self.writer.writeheader()


    def print_competitors(self):
        print(self.competitors)


    def close_out_file(self):
        self.out_file.close()


    def check_valid_competitor_count(self, num_competitors):
        num_rounds = math.log(num_competitors, 2)

        if num_rounds - round(num_rounds) != 0:
            raise ValueError(f"Number of competitors must be a power of 2! Current number of competitors: {num_competitors}")


    def create_bracket(self, competitors):
        unassigned_competitiors = competitors
        num_competitors = len(unassigned_competitiors)
        self.check_valid_competitor_count(num_competitors)
        bracket = {}

        matches_in_round = int(num_competitors / 2)

        #TODO: Check that num competitors is a power of 2

        for c in range(1, matches_in_round + 1):
            n = len(unassigned_competitiors)
            bracket[c] = [unassigned_competitiors.pop(n-1)[0], unassigned_competitiors.pop(0)[0]]

        return bracket


    def initiate_tournament(self, bracket, stage):
        num_matches = len(bracket)
        print(f"Round {stage} starting now. Number of matches in current round is {num_matches}.\n")
        winners = []

        for i in range(1, num_matches + 1):
            winner = input(f"Vote for the winner: {bracket[i][1]} (1) vs {bracket[i][0]} (0) !\n")
            print(f"{bracket[i][int(winner)]} wins!")
            self.writer.writerow({'round': stage, 'match_number': i, 'c1': bracket[i][0], 'c2': bracket[i][1], 'winner': bracket[i][int(winner)]})
            print("\n")
            winners.append([bracket[i][int(winner)]])

        if num_matches > 1:
            next_round = self.create_bracket(winners)
            self.initiate_tournament(next_round, stage + 1)
        elif num_matches == 1:
            print(f"{winners[0][0]} wins the tournament!")

def main():

    num_args = len(sys.argv[1:])

    competitors_path = sys.argv[1]

    if num_args > 1:
        max_competitors = int(sys.argv[2])
    else:
        max_competitors = None

    obj = DecideByBracket(competitors_path, max_competitors)

    starting_bracket = obj.create_bracket(obj.competitors)

    obj.initiate_tournament(starting_bracket, 1)

    obj.close_out_file()

if __name__ == "__main__":
    main()
        
    