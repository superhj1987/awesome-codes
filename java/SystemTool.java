import java.io.IOException;

public class SystemTool {
    public static void killByPid(String str) {
        final String[] Array = {"ntsd.exe", "-c", "q", "-p", str};
        int i = 0;
        try {
            Process process = Runtime.getRuntime().exec(Array);
            process.waitFor();
        } catch (InterruptedException e) {
            System.out.println("run err!");
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }

        if (i != 0) {
            try {
                Process process = Runtime.getRuntime().exec(Array);
                process.waitFor();
            } catch (InterruptedException e) {
                System.out.println("err!");
                e.printStackTrace();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }
}
