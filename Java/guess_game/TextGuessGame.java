public class TextGuessGame extends GuessGame{
    public static int totalGuessCount = 0;
    private java.util.Scanner scanner;
    public TextGuessGame(){ 
        scanner = new java.util.Scanner(System.in); 
    }
    public void bigger(){ 
        System.out.println("輸入數字比較目標數字大"); 
    }
    public void smaller(){
        System.out.println("輸入數字比較目標數字小");
    }
    public void right(){
        System.out.println("恭喜!猜中了!");
    }
    public int userInput(){
        System.out.print("輸入數字: ");
        totalGuessCount++;
        return scanner.nextInt();
    }
}