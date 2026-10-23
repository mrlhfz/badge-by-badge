type ErrorStateProps = {
    message: string;
    onRetry?: () => void;
};

export default function ErrorState({ message, onRetry }: ErrorStateProps) {
    return (
        <div role="alert">
            <p>{message}</p>
            {onRetry && <button onClick={onRetry}>Try again</button>}
        </div>
    );
}
