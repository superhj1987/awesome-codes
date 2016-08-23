public class TextUtil{
  public static getStrWidth(){
    //计算出当前绘制出来的字符串有多宽，可以这么来！
    //方法1：
    Paint pFont = new Paint();
    Rect rect = new Rect();

    //返回包围整个字符串的最小的一个Rect区域
    pFont.getTextBounds(str, 0, 1, rect);

    return rect.width();

    //方法2：

    //直接返回参数字符串所占用的宽度
    //return paintHead.measureText(str);
  }
}
