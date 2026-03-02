import { FC, ReactNode } from "react";
import { colors, typography } from "@/styles/theme";

interface PageHeaderProps {
  title: string;
  subtitle?: string;
  actions?: ReactNode;
}

const PageHeader: FC<PageHeaderProps> = ({ title, subtitle, actions }) => {
  return (
    <div style={{ marginBottom: '2rem' }}>
      <div style={{ 
        display: 'flex', 
        justifyContent: 'space-between', 
        alignItems: 'center',
        marginBottom: '0.5rem',
        gap: '1rem',
        flexWrap: 'wrap'
      }}>
        <h1
          style={{
            margin: 0,
            fontSize: typography.fontSize['3xl'],
            fontWeight: typography.fontWeight.bold,
            color: colors.text.primary,
            fontFamily: typography.fontFamily.heading,
            letterSpacing: typography.letterSpacing.tight,
            lineHeight: 1.2,
          }}
        >
          {title}
        </h1>
        {actions}
      </div>
      {subtitle && (
        <p
          style={{
            margin: 0,
            color: colors.text.secondary,
            fontSize: typography.fontSize.base,
            fontWeight: typography.fontWeight.normal,
          }}
        >
          {subtitle}
        </p>
      )}
    </div>
  );
};

export default PageHeader;
