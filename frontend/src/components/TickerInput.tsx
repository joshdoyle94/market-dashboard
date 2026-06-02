import { useRef } from "react";

interface TickerInputProps {
  onSetTicker: (ticker: string) => void;
}

export default function TickerInput({ onSetTicker }: TickerInputProps) {
  const inputRef = useRef<HTMLInputElement>(null);

  const submit = () => {
    const ticker = inputRef.current?.value.trim().toUpperCase();
    if (ticker) {
      onSetTicker(ticker);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter") {
      submit();
    }
  };

  return (
    <div style={{ display: "flex", gap: "8px" }}>
      <input
        ref={inputRef}
        type="text"
        onKeyDown={handleKeyDown}
        placeholder="Enter ticker"
        style={{ border: "1px solid black", padding: "6px 8px" }}
      />
      <button
        onClick={submit}
        style={{ border: "1px solid black", padding: "6px 12px" }}
      >
        Go
      </button>
    </div>
  );
}