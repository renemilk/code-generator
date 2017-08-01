#pragma once 

#include <string>
#include <array>

#ifdef __CODE_GENERATOR__
#define HIDDEN __attribute__((annotate("hidden")))
#else
#define HIDDEN
#endif

class TextComponent  
{
public:
    TextComponent();
//
//    std::string text() const;
//    double** doublepointer() const;
//    void setText(const std::string& value);
//
//    HIDDEN void superSecretFunction();
//
//    static int myStatic();

    template <typename T, int size>
    std::array<T,size> tplFunc(int loc, T ui);

    template <typename T, int size>
    std::array<T,size> definedFunc(int loc, T ui) {
    }

private:

    void privFunction();
    std::string m_text;
};
