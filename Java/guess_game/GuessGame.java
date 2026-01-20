public abstract class GuessGame {
    private int number;
    public void setNumber(int number) { this.number = number; }

    public void start() {
        int guess = 0;
        do {
            guess = userInput();
            if (guess > number) bigger();
            else if (guess < number) smaller();
            else right();
        } while (guess != number);
    }
    protected abstract void bigger();
    protected abstract void smaller();
    protected abstract void right();
    protected abstract int userInput();
}