import { colors, typography } from "@/styles/theme";
import { MantineStyleProps, Title as MantineTitle } from "@mantine/core"
import { FC, PropsWithChildren } from "react"

interface TitleProps extends PropsWithChildren, MantineStyleProps {
  order?: 1 | 2 | 3 | 4 | 5 | 6;
  fontSize?: keyof typeof typography.fontSize;
}

const Title: FC<TitleProps> = ({
  children,
  order = 1,
  fontSize,
  mb,
}) => {
  return (
    <MantineTitle
      mb={mb}
      order={order}
      style={{
        color: colors.primary.main,
        fontSize: fontSize ? typography.fontSize[fontSize] : undefined,
        fontWeight: typography.fontWeight.bold,
      }}
    >
      {children}
    </MantineTitle>
  )
}

export default Title;