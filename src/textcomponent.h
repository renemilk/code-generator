#pragma once 

#include <string>

#ifdef __CODE_GENERATOR__
#define HIDDEN __attribute__((annotate("hidden")))
#else
#define HIDDEN
#endif

class TextComponent  
{
public:
    TextComponent();

    std::string text() const;
    double** doublepointer() const;
    void setText(const std::string& value);

    HIDDEN void superSecretFunction();

    static int myStatic();

private:

    void privFunction();
    std::string m_text;
};
