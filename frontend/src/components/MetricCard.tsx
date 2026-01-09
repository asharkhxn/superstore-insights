interface MetricCardProps {
  title: string;
  value: number;
  format?: "currency" | "number" | "percent";
}

export default function MetricCard({
  title,
  value,
  format = "number",
}: MetricCardProps) {
  const formatValue = (val: number): string => {
    switch (format) {
      case "currency":
        return `$${val.toLocaleString("en-US", {
          minimumFractionDigits: 0,
          maximumFractionDigits: 0,
        })}`;
      case "percent":
        return `${val.toFixed(2)}%`;
      default:
        return val.toLocaleString("en-US");
    }
  };

  return (
    <div className="metric-card">
      <h3>{title}</h3>
      <div className="value">{formatValue(value)}</div>
    </div>
  );
}
