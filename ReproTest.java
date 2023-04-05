import com.google.errorprone.annotations.CheckReturnValue;

public final class ReproTest {
    @CheckReturnValue
    public static int foo() {
        return 0;
    }
}
