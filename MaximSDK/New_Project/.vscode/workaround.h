/*
This is a workaround to VS Code's unresolved issues defining platform-specific symbols
even when the compiler is specified.  By force-including
this file we can get the intellisense engine to stop including
non-existent system header files.

https://github.com/microsoft/vscode-cpptools/issues/1083
https://github.com/microsoft/vscode-cpptools/issues/4653


*/

#undef _WIN32
#undef __GNUG__
#undef __cplusplus
#undef __clang__
#undef __clang_major__
#undef __clang_minor__
#undef __clang_patchlevel__
