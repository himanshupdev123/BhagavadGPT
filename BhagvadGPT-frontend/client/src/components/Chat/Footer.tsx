import React, { useEffect, memo, useState } from 'react';
import TagManager from 'react-gtm-module';
import ReactMarkdown from 'react-markdown';
import { Constants } from 'librechat-data-provider';
import { useGetStartupConfig } from '~/data-provider';
import { useLocalize } from '~/hooks';

function Footer({ className }: { className?: string }) {
  const { data: config } = useGetStartupConfig();
  const localize = useLocalize();
  const [questionCount, setQuestionCount] = useState<number | null>(null);

  // Fetch question count from backend
  useEffect(() => {
    const fetchQuestionCount = async () => {
      try {
        const response = await fetch('http://localhost:8000/api/question-stats');
        const data = await response.json();
        if (data.success) {
          setQuestionCount(data.total_questions);
        }
      } catch (error) {
        console.error('Failed to fetch question count:', error);
      }
    };

    // Initial fetch
    fetchQuestionCount();

    // Refresh every 30 seconds
    const interval = setInterval(fetchQuestionCount, 30000);

    return () => clearInterval(interval);
  }, []);

  const privacyPolicy = config?.interface?.privacyPolicy;
  const termsOfService = config?.interface?.termsOfService;

  const privacyPolicyRender = privacyPolicy?.externalUrl != null && (
    <a className="text-text-secondary underline" href={privacyPolicy.externalUrl} rel="noreferrer">
      {localize('com_ui_privacy_policy')}
    </a>
  );

  const termsOfServiceRender = termsOfService?.externalUrl != null && (
    <a className="text-text-secondary underline" href={termsOfService.externalUrl} rel="noreferrer">
      {localize('com_ui_terms_of_service')}
    </a>
  );

  const mainContentParts = (
    typeof config?.customFooter === 'string'
      ? config.customFooter
      : 'BhagvadGPT can make mistakes. Please read the  Bhagavad Gita'
  ).split('|');

  useEffect(() => {
    if (config?.analyticsGtmId != null && typeof window.google_tag_manager === 'undefined') {
      const tagManagerArgs = {
        gtmId: config.analyticsGtmId,
      };
      TagManager.initialize(tagManagerArgs);
    }
  }, [config?.analyticsGtmId]);

  const mainContentRender = mainContentParts.map((text, index) => (
    <React.Fragment key={`main-content-part-${index}`}>
      <ReactMarkdown
        components={{
          a: ({ node: _n, href, children, ...otherProps }) => {
            return (
              <a
                className="text-text-secondary underline"
                href={href}
                rel="noreferrer"
                {...otherProps}
              >
                {children}
              </a>
            );
          },

          p: ({ node: _n, ...props }) => <span {...props} />,
        }}
      >
        {text.trim()}
      </ReactMarkdown>
    </React.Fragment>
  ));

  const footerElements = [...mainContentRender, privacyPolicyRender, termsOfServiceRender].filter(
    Boolean,
  );

  return (
    <div
      className={
        className ??
        'absolute bottom-0 left-0 right-0 flex flex-col items-center justify-center gap-2 px-2 py-2 text-center text-xs text-text-primary md:px-[60px]'
      }
      role="contentinfo"
    >
      {/* Question counter - displayed above existing footer */}
      {questionCount !== null && (
        <div className="text-black text-xs mb-1">
          BhagvadGPT has Gitafied {questionCount.toLocaleString()} Questions to date.
        </div>
      )}

      {/* Existing footer content - responsive layout */}
      <div className="flex flex-col sm:flex-row items-center justify-center gap-2 flex-wrap">
        {footerElements.map((contentRender, index) => {
          const isLastElement = index === footerElements.length - 1;
          return (
            <React.Fragment key={`footer-element-${index}`}>
              {contentRender}
              {!isLastElement && (
                <div
                  key={`separator-${index}`}
                  className="hidden sm:block h-2 border-r-[1px] border-border-medium"
                />
              )}
            </React.Fragment>
          );
        })}
      </div>
    </div>
  );
}

const MemoizedFooter = memo(Footer);
MemoizedFooter.displayName = 'Footer';

export default MemoizedFooter;
