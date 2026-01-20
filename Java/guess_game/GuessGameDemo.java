// 這一段是執行程式必須要有的「進入點」
public class GuessGameDemo {
    public static void main(String[] args) {
            GuessGame game = new TextGuessGame();
            game.setNumber(50); // 設定要猜的目標數字
            game.start();      // 開始遊戲
            System.out.println("總共猜了 " + TextGuessGame.totalGuessCount + " 次");
    }

}


