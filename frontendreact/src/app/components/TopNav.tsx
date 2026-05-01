import { Search, Bell, User, Globe } from 'lucide-react';
import { useState } from 'react';

export function TopNav() {
  const [language, setLanguage] = useState('EN');

  return (
    <header className="h-16 bg-white/80 backdrop-blur-xl border-b border-[#20AA99]/10 shadow-sm">
      <div className="h-full px-8 flex items-center justify-between">
        {/* AVA Logo and Title */}
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-[#20AA99] to-[#2F748E] flex items-center justify-center shadow-lg">
              <span className="text-white font-bold text-xl">A</span>
            </div>
            <div>
              <h1 className="font-bold text-[#2F748E] text-lg">AVA</h1>
              <p className="text-xs text-[#20AA99]">AI Medical Excellence Platform</p>
            </div>
          </div>
        </div>

        {/* Search Bar */}
        <div className="flex-1 max-w-xl mx-8">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-[#2F748E]/40" />
            <input
              type="text"
              placeholder="Search..."
              className="w-full pl-10 pr-4 py-2 rounded-lg bg-white border border-[#20AA99]/20 focus:outline-none focus:ring-2 focus:ring-[#20AA99]/50 focus:border-transparent transition-all text-[#2F748E]"
            />
          </div>
        </div>

        {/* Right side actions */}
        <div className="flex items-center gap-4">
          {/* Language Selector */}
          <div className="flex items-center gap-2 px-3 py-2 rounded-lg bg-white border border-[#20AA99]/20">
            <Globe className="w-4 h-4 text-[#20AA99]" />
            <select
              value={language}
              onChange={(e) => setLanguage(e.target.value)}
              className="bg-transparent text-sm text-[#2F748E] focus:outline-none cursor-pointer"
            >
              <option value="EN">EN</option>
              <option value="FR">FR</option>
              <option value="AR">AR</option>
            </select>
          </div>

          {/* Notifications */}
          <button className="relative p-2 rounded-lg hover:bg-[#F4FBFF] transition-colors">
            <Bell className="w-5 h-5 text-[#2F748E]" />
            <span className="absolute top-1 right-1 w-2 h-2 bg-[#20AA99] rounded-full"></span>
          </button>

          {/* User Profile */}
          <div className="flex items-center gap-3 px-3 py-2 rounded-lg bg-gradient-to-r from-[#20AA99] to-[#2F748E] text-white">
            <div className="w-8 h-8 rounded-full bg-white/20 flex items-center justify-center">
              <User className="w-5 h-5" />
            </div>
            <div className="text-sm">
              <p className="font-medium">Medical Manager</p>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
}
