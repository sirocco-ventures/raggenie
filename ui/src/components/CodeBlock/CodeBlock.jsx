import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter'; // Prism highlighter
import { solarizedlight } from 'react-syntax-highlighter/dist/cjs/styles/prism';
import Button from '../Button/Button';
import { PiCopySimpleBold } from 'react-icons/pi';
import style from './CodeBlock.module.css'; // Import the CSS module

const CodeBlock = ({ codeString = "", Codestyle }) => {
  const customTheme = {
    ...solarizedlight, // Use the base solarizedlight theme
    'comment': { color: '#888787' }, // Customize comment color
    'variable': { color: '#ff0000' }, // Customize variable color
  };

  const customStyle = {
    lineHeight: '1.5',
    fontSize: '1rem',
    borderRadius: '6px',
    background: '#F9F9F9',
    padding: '20px',
    width: '100%', // Make code block width responsive
    height: '260px'
  };

  const copyToClipboard = () => {
    navigator.clipboard.writeText(codeString)
      .catch(err => console.error("failed to copy", err))
  }

  return (
    <div className={style.CodeBlockContainer} style={Codestyle} onClick={copyToClipboard}>
      <Button type="solid" className={`${style.LightButton}`} >
        <span>Copy Code</span>
        <span><PiCopySimpleBold size={18} /></span>
      </Button>

      <SyntaxHighlighter language='javascript' style={customTheme} customStyle={customStyle}>
        {codeString}
      </SyntaxHighlighter>
    </div>
  );
};

export default CodeBlock;
