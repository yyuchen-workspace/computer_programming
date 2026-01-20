void main(){
  runApp(App());
}

class App extends StatelessWidget{
  @override
  Widget build(BuildContext context){
    return MaterialApp(
      title: '計算機',
      home: CalculatorPage(),
    );
  }
}
class CalculatorPage extends StatefulWidget{
  @override
  _CalculatorPageState createState() => _CalculatorPageState();
}